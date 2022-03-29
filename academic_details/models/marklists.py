from odoo import fields,models,api, _
from datetime import datetime, date
from odoo.exceptions import ValidationError, UserError, Warning

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    sale_by = fields.Selection([('weight', 'Weight()'), ('unit', 'Units')], string='Sale By')
    delivery_date = fields.Date(string='Expected Delivery Date')
    discount_type = fields.Selection([('fixed', 'Fixed Price'), ('percent', 'Percentage')], string='Discount Type')
    discount_percent = fields.Float(string='Discount')
    fixed_amt = fields.Float(string='Fixed Amount')
    total_discount = fields.Float(string='Total Discount', compute='_amount_all')
    # test_fld = fields.Text("Test Text")

    @api.depends('discount_percent', 'amount_total', 'fixed_amt')
    def _amount_all(self):
        res = super(SaleOrderInherit, self)._amount_all()
        for rec in self:
            if rec.discount_type == 'percent':
                rec.total_discount = rec.amount_total*(rec.discount_percent / 100)
                rec.amount_total = rec.amount_untaxed - rec.total_discount
            else:
                rec.total_discount = rec.fixed_amt
                rec.amount_total = rec.amount_untaxed - rec.fixed_amt
        return res

    # @api.model
    def action_confirm(self):
        result = super(SaleOrderInherit, self).action_confirm()
        stock_pick = self.env["stock.picking"].search([('origin', '=', self.name)])

        for line in stock_pick:
            line.write({'sale_by_so': self.sale_by,
                        'delivery_date_so': self.delivery_date
                        })
        return result

    def test_product(self):
        print(1111)
        # ids = [23, 44, 15, 29,16, 18,10,9,28,8]
        # cid = [1,1,1,1,2,1,2,1,1,1]
        # product = self.env['product.template'].search([('id', 'in', ids)])
        # company = self.env['res.company'].search([('id', 'in', cid)])
        # if product:
        #     print(product, "pppp//>>>>>>>>>>", company)
        #     for pro in product:
        #         pro.write({
        #             'company_id': cid,
        #         })
        # return True

class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    # @api.onchange('product_id')
    # def onchange_price(self):
    #     if self.product_id:
    #       for rec in self.order_id:
    #         sum_sub = sum(li.price_subtotal for li in self)
    #         rec.amount_untaxed = sum_sub

class DeliveryOrder(models.Model):
    _inherit = 'stock.picking'

    sale_by_so = fields.Selection([('weight', 'Weight(kg)'), ('unit', 'Units')], string='Sale By')
    delivery_date_so = fields.Date(string='Expected Delivery Date')

    def action_view_invoice(self):
        invoices = self.mapped('invoice_ids')
        action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_out_invoice_type")
        if len(invoices) > 1:
            action['domain'] = [('id', 'in', invoices.ids)]
        elif len(invoices) == 1:
            form_view = [(self.env.ref('account.view_move_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = invoices.id
        else:
            action = {'type': 'ir.actions.act_window_close'}

        return action

    def action_sale(self):
        rec = self.env['sale.order'].search([('name', '=', self.origin)])
        if rec:
            return {
                    'view_mode': 'form',
                    'view_type': 'form',
                    'res_model': 'sale.order',
                    'type': 'ir.actions.act_window',
                    'res_id': rec.id,
                    #'nodestroy': True,
                    'target': 'current'
                }

    def action_create_invoice(self):
        # if self.sale_id.invoice_ids:
        #     raise UserError("Invoice Already raised from Sale Order")
        sale = self.env['sale.order'].search([('name', '=', self.origin)])
        if sale.invoice_count > 0:
            raise UserError("Invoice Already raised from Sale Order")
        
        if self.state !="done":
            raise UserError("Please Validate the product details first")
        
        if not self.partner_id:
            raise UserError("Please add delivery address details")
        
        # get journal
        journal_id = self.env['account.journal'].sudo().search([('type','=','sale'),('company_id','=',self.company_id.id)],limit=1)
        if not journal_id:
            raise UserError("Please configure sales journal for company:{}".format(self.company_id.name))
        
        # prepare line
        account_move_line = []
        for line_id in self.move_line_ids_without_package:
            account_move_line.append((0,0,{
                'product_id':line_id.product_id.id,
                'quantity':line_id.qty_done,
                'price_unit':line_id.move_id.sale_line_id.price_unit if line_id.move_id.sale_line_id else line_id.product_id.lst_price,
                'account_id': journal_id.default_account_id.id if journal_id.default_account_id else False,
                'name':line_id.product_id.name,
                'discount': line_id.move_id.sale_line_id.discount,
                # 'product_specification':line_id.move_id.sale_line_id.product_specification.id if line_id.move_id.sale_line_id else False,
                'product_uom_id': line_id.product_uom_id.id if line_id.product_uom_id else False,
            }))
        if not account_move_line:
            raise UserError("No lines found to create invoice")
        # create invoice
        
        create_invoice = self.env['account.move'].sudo().create(
            {
                'move_type':'out_invoice',
                'partner_id': self.partner_id.id if self.partner_id else False,
                'invoice_date_due': date.today(),
                'journal_id': journal_id.id,
                # 'picking_id': self.id,
                'state':'draft',
                'invoice_line_ids': account_move_line ,
                'invoice_origin': self.origin,
                # 'discount_type': sale.discount_type,
                # 'discount_rate': sale.discount_rate,
            }
        )
        ac_move = self.env['account.move'].search([('invoice_origin','=', self.origin)])
        # sale = self.env['sale.order'].search([('name', '=', 'origin')])
        ac_move = self.env['account.move'].search([('invoice_origin', '=', 'origin')])
        if ac_move:
            for order_line in sale.order_line:
                print(ac_move, "===9999999999999")
                ac_move.write({
                   'discount_type': order_line.discount_type,
                #    'amount_discount': sale.amount_discount,
                #    'margin': sale.amount_total,
                })
            
        if create_invoice:
            self.invoice_created = True
            if self.sale_id:
                self.sale_id._get_invoice_status()
                invoiced = False
                partially_invoiced = False
                for picking in self.sale_id.picking_ids:
                    if picking.invoice_created:
                        invoiced = True
                    else:
                        partially_invoiced = True
                    
                if invoiced and partially_invoiced:
                    self.sale_id.invoice_status = "partially_invoiced"
                elif invoiced:
                    self.sale_id.invoice_status = "invoiced"
        
        # return self.action_view_invoice()
        # action = self.env["ir.actions.actions"]._for_xml_id("sale.action_quotations_with_onboarding")
        # obj = self.env['sale.order'].search([('name', '=', self.origin)])
        # if obj:
        #     form_view = [(self.env.ref('sale.view_order_form').id, 'form')]
        #     # if 'views' in action:
        #     action['views'] = form_view
        #     action['res_id'] = obj.id
        #     action['domain'] = [('name', '=', self.origin)]
        
        # return action
        
        
class SaleAdvancePaymentInherit(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def create_invoices(self):
        res = super(SaleAdvancePaymentInherit, self).create_invoices()
        sale = self.env['sale.order'].browse(self.env.context.get('active_id'))
        ac_move = self.env['account.move'].search([('invoice_origin', '=', sale.name)], limit=1)
        if self.advance_payment_method == 'fixed' or 'percentage':
            for line in sale.order_line:
                if line.product_id.name != 'Down payment':
                    ac_move.invoice_line_ids.create({
                'product_id': line.product_id.id,
                'name': line.name,
                'account_id': 78,
                'move_id': ac_move.id,
                  })
                # else:
                #     break

        return res

class StudentsMarklist(models.Model):
    _name = 'student.marklists'

    name = fields.Char(string='Students Name')
    standard = fields.Integer(string='Standard')

    mark2 = fields.Integer(string='Maths')
    mark3 = fields.Integer(string='Science')
    mark4 = fields.Integer(string='Computer Science')
    section = fields.Selection([('secA', 'A'), ('secB', 'B'),
                              ('secC', 'C')], string='Section')


class AccountProducts(models.Model):
    _inherit = 'account.move'

    @api.onchange('partner_id')
    def onchange_gang_payslip(self):
        for rec in self:
            lines = [(5, 0, 0)]
            #print("self.gang_payslip", self.gang_payslip.gang_emp_name)
            for line in self.invoice_line_ids:
                val = {
                    'product_id': line.product_id.id
                }
                lines.append((0, 0, val))
            print('lines', lines)
            rec.invoice_line_ids = lines


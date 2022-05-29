from odoo import tools
from odoo import fields, models, api, _
# import odoo.addons.decimal_precision as dp
import datetime
import logging
# from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class sale_move_analysis(models.Model):
	_name = "vit.move.analysis"

	categ_id = fields.Many2one('product.category', 'Category')
	model_id = fields.Many2one('vit.master.type', 'Model')
	product_id = fields.Many2one('product.product', 'Product')
	onhand_qty = fields.Integer('OnHand Qty')
	in_qty = fields.Integer('Total In Qty')
	out_qty = fields.Integer('Total Out Qty')
	soh_qty = fields.Integer('Total SOH Qty')
	out_qty_cust = fields.Integer('Out Qty Customer')
	in_qty_qc = fields.Integer('In Qty QC')
	year = fields.Char('Year')
	month = fields.Char('Month')
	day = fields.Char('Day')
	location_id = fields.Many2one('stock.location', 'Location')

# class sale_move_analysis_onhand(models.Model):
# 	_name = "vit.move.analysis.onhand"

# 	categ_id = fields.Many2one('product.category', 'Category')
# 	model_id = fields.Many2one('vit.master.type', 'Model')
# 	product_id = fields.Many2one('product.product', 'Product')
# 	onhand_qty = fields.Integer('OnHand Qty')
# 	date = fields.Char("Date")
#     location_id = fields.Many2one('stock.location','Location')


class sale_move_analysis_onhand(models.Model):
    _name = "vit.move.analysis.onhand"
    
    categ_id = fields.Many2one('product.category', 'Category')
    model_id = fields.Many2one('vit.master.type', 'Model')
    product_id = fields.Many2one('product.product', 'Product')
    onhand_qty = fields.Integer('OnHand Qty')
    date = fields.Char("Date")
    location_id = fields.Many2one('stock.location','Location')				
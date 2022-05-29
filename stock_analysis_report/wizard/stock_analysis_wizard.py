from odoo import models,fields, _
# from odoo.tools.translate import _
import datetime 

class report_wizard(models.TransientModel): 
	_name = 'vit_move_analysis.report_wizard' 

	date_from = fields.Date('Date from',required=True)
	date_to = fields.Date('Date to',required=True)
	location_id = fields.Many2one('stock.location','Location',required=True)
	type = fields.Selection([('move','Move Analysis'),('inventory','Inventory Analysis')],'Type',required=True)

	# _defaults = {
	# 	'date_from'  : fields.date.context_today,
	# 	'date_to'  : fields.date.context_today,
	# 	'location_id'    : 14,#Lokasi Barang Jadi	
	# }

	def fill_table(self):
		location = self.location_id.id
		date_from = self.date_from
		date_to = self.date_to
		tp = self.type

		if tp == 'move' :
			sql = "delete from vit_move_analysis"
			self.env.cr.execute(sql)
			sql = """INSERT INTO vit_move_analysis( 
						categ_id,
						product_id ,
						onhand_qty,
						in_qty ,
						out_qty,
						in_qty_qc,
						out_qty_cust,						
						soh_qty,						
						year ,
						month,
						day,
						location_id
						)
							select
								tmpl.categ_id as categ,
								sm.product_id as product,
								((select sum(product_qty) as source_qty from stock_move where location_dest_id=%s and state='done' and product_id=sm.product_id and to_char(date, 'YYYY-MM-DD') <= '%s')-
								(select sum(product_qty) as dest_qty from stock_move where location_id=%s and state='done' and product_id=sm.product_id and to_char(date, 'YYYY-MM-DD') <= '%s')
								) as onhand_qty,
								(select sum(product_qty) as in_qty from stock_move where location_dest_id=%s 
									and state='done' and product_id=sm.product_id and id = sm.id and(date between '%s' and '%s')) as in_qty,
								(select sum(product_qty) as out_qty from stock_move where location_id=%s 
									and state='done' and product_id=sm.product_id and id = sm.id and(date between '%s' and '%s')) as out_qty,
								((select sum(product_qty) as in_qty_qc from stock_move where location_dest_id=%s and location_id=29
									and state='done' and product_id=sm.product_id and id = sm.id and(date >= '%s' and date <='%s'))-
								coalesce((select sum(product_qty) as in_qty_qc from stock_move where location_dest_id=29 and location_id=%s
									and state='done' and product_id=sm.product_id and id = sm.id and(to_char(date, 'YYYY-MM-DD') >= '%s' and to_char(date, 'YYYY-MM-DD') <= '%s')),0))  as in_qty_qc,
								((select sum(product_qty) as out_qty_cust from stock_move where location_id=%s and location_dest_id=9
									and state='done' and product_id=sm.product_id and id = sm.id and(date >= '%s' and date <='%s'))-
								coalesce((select sum(product_qty) as out_qty_cust from stock_move where location_id=9 and location_dest_id=%s
									and state='done' and product_id=sm.product_id and id = sm.id and(to_char(date, 'YYYY-MM-DD') >= '%s' and to_char(date, 'YYYY-MM-DD') <= '%s')),0)) as out_qty_cust,							
								
								(   COALESCE((((select sum(product_qty) as source_qty from stock_move where location_dest_id=%s and state='done' and product_id=sm.product_id and to_char(date, 'YYYY-MM-DD') <= '%s')-
								(select sum(product_qty) as dest_qty from stock_move where location_id=%s and state='done' and product_id=sm.product_id and to_char(date, 'YYYY-MM-DD') <= '%s')
								)),0)+
								COALESCE((((select sum(product_qty) as in_qty_qc from stock_move where location_dest_id=%s and location_id=29
									and state='done' and product_id=sm.product_id and id = sm.id and(date >= '%s' and date <='%s'))-
								coalesce((select sum(product_qty) as in_qty_qc from stock_move where location_dest_id=29 and location_id=%s
									and state='done' and product_id=sm.product_id and id = sm.id and(to_char(date, 'YYYY-MM-DD') >= '%s' and to_char(date, 'YYYY-MM-DD') <= '%s')),0))),0)-
								COALESCE((((select sum(product_qty) as out_qty_cust from stock_move where location_id=%s and location_dest_id=9
									and state='done' and product_id=sm.product_id and id = sm.id and(date >= '%s' and date <='%s'))-
								coalesce((select sum(product_qty) as out_qty_cust from stock_move where location_id=9 and location_dest_id=%s
									and state='done' and product_id=sm.product_id and id = sm.id and(to_char(date, 'YYYY-MM-DD') >= '%s' and to_char(date, 'YYYY-MM-DD') <= '%s')),0))),0)   ) as soh,
								to_char(sm.date, 'YYYY') as year,
								to_char(sm.date, 'MM') as month,
								to_char(sm.date, 'YYYY-MM-DD') as day,
								%s as location_id
							from stock_move sm
								left join mrp_bom mb on sm.product_id=mb.product_id
								left join product_product pp on sm.product_id = pp.id
								left join product_template tmpl on pp.product_tmpl_id = tmpl.id 
							where 
								(sm.location_id=%s or sm.location_dest_id=%s)
								and sm.state='done' and sm.date between '%s' and '%s'
							group by sm.date,sm.product_id,tmpl.categ_id,sm.id
				
						""" % (
							location,
							date_to,
							location,
							date_to,

							location,
							date_from,
							date_to,

							location,
							date_from,
							date_to,

							location,

							date_from,
							date_to,
							location,
							date_from,

							date_to,
							location,
							date_from,
							date_to,

							location,
							date_from,
							date_to,

							location,
							date_to,
							location,
							date_to,

							location,
							date_from,
							date_to,
							location,
							date_from,
							date_to,

							location,
							date_from,
							date_to,
							location,
							date_from,
							date_to,

							location,
							location,

							location,
							date_from,
							date_to
							)

			self.env.cr.execute(sql)
			view_id = self.env.ref('stock_analysis_report.view_vit_move_analysis_tree').id
			# view_id = view_ref and view_ref[1] or False,		
			return {
				'name' : _('Move Analysis '+str(self.date_from)+' to '+str(self.date_to)+' '+str(self.location_id.name)),
				# 'view_type': 'form',
				'view_mode': 'tree,pivot',			
				'res_model': 'vit.move.analysis',
				# 'res_id': ids[0],
				'type': 'ir.actions.act_window',
				# 'view_id': view_id,
				'res_model':'vit.move.analysis',
				'target': 'current',
				'domain' : "[]",
				'context': '{"search_default_location_id":1,"search_default_day":1}',
				'nodestroy': False,
				}

		else:
			sql = "delete from vit_move_analysis_onhand"
			self.env.cr.execute(sql)
			sql = """INSERT INTO vit_move_analysis_onhand( 
						categ_id,
						product_id ,
						onhand_qty,
						date,
						location_id
						)
						select
								tmpl.categ_id as categ,
								pp.id as product,
								((select sum(product_qty) as source_qty from stock_move where location_dest_id=%s and state='done' and product_id=pp.id and date <= '%s')-
								(select sum(product_qty) as source_qty from stock_move where location_id=%s and state='done' and product_id=pp.id and date <= '%s')
								) as onhand_qty,
								'%s' as date,
								%s as location_id 
						from		
							product_product pp 
							left join product_template tmpl on pp.product_tmpl_id = tmpl.id 
							left join mrp_bom mb on pp.id=mb.product_id
						group by pp.id, tmpl.categ_id
						""" % (location,date_to,location,date_to,date_to,location)

			self.env.cr.execute(sql)

			# view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'stock_analysis_report', 'view_vit_move_analysis_onhand_tree')
			view_id = self.env.ref('stock_analysis_report.view_vit_move_analysis_onhand_tree').id		
			return {
				'name' : _('Inventory Analysis '+str(self.date_from)+' to '+str(self.date_to)+' '+str(self.location_id.name)),
				# 'view_type': 'form',
				'view_mode': 'tree',			
				'res_model': 'vit.move.analysis.onhand',
				# 'res_id': ids[0],
				'type': 'ir.actions.act_window',
				'view_id': view_id,
				'target': 'current',
				'domain' : "[]",
				'context': '{"search_default_categ_id":1}',
				'nodestroy': False,
				}
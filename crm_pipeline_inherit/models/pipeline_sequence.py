from odoo import api, fields, models, _
from datetime import datetime, timedelta


class CRMPipeline(models.Model):
	_inherit="crm.lead"
	
	pipeline_seq = fields.Char(string="Sequence", default='New')
	new_seq = fields.Char(string="name")

	@api.model
	def create(self,vals):
		# create the sequence number for crm lead
		if vals.get("pipeline_seq","New") == "New":
			
			vals["pipeline_seq"]= self.env["ir.sequence"].next_by_code("crm.lead.seq") or "New"

		res = super(CRMPipeline, self).create(vals)		
		return res

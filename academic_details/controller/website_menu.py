from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class Student(http.Controller):

    @http.route('/student_webform', type="http", auth="public", website=True)
    def student_webform(self, **kw):
        print("sssssssDONEssssssss...............")
        return http.request.render('academic_details.create_student', {})

    @http.route('/create/webstudent', type="http", auth="public", website=True)
    def create_webstudent(self, **kw):
        print("////////////////ok//////////////", kw)
        request.env['student.marklists'].sudo().create(kw)
        student_val = {
            'name': kw.get('name'),
            'standard': kw.get('standard')
        }
        request.env['student.marklists'].sudo().create(student_val)
        return request.render("academic_details.confirmation", {})

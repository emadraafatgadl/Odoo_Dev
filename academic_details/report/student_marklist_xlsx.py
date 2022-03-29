from odoo import models


class StudentMarklistXL(models.AbstractModel):
    _name = 'report.academic_details.report_ticket_action_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        print('lines', lines)
        format1 = workbook.add_format({'font_size': 10, 'align': 'vcenter', 'bold': True})
        format2 = workbook.add_format({'font_size': 8, 'align': 'vcenter'})
        sheet = workbook.add_worksheet('Student Marklist')
        sheet.write(0, 0, 'Name', format1)
        sheet.write(0, 1, 'Standard', format1)
        sheet.write(0, 2, 'Maths', format1)
        sheet.write(0, 3, 'Science', format1)
        sheet.write(0, 4, 'Computer', format1)
        sheet.write(1, 0, lines.name, format2)
        sheet.write(1, 1, lines.standard, format2)
        sheet.write(1, 2, lines.mark2, format2)
        sheet.write(1, 3, lines.mark3, format2)
        sheet.write(1, 4, lines.mark4, format2)


# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Academic Master',
    'version': '14.0',
    'summary': 'requesting module',
    'sequence': 14,
    'description': """
    This module is used to request a loan to the authority and the loan approver from the other end will decide to either approve or reject the loan request 
        """,
    'category': 'Finance',
    'website': 'https://www.odoo.com/page/billing',
    'depends': ['base', "sale", "crm", "stock","website"],
    'data': [
        'security/ir.model.access.csv',
        'views/student_marklist.xml',
        'views/website_form _view.xml',
        'views/custom_snippets.xml'

      
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Stock Analysis Report',
    'version': '13.0',
    'category': 'Inventory/Product',
    'sequence': 35,
    'summary': 'Inventory orders, tenders and agreements',
    'description': "",
    'depends': ['stock', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_analysis_view.xml',
        'wizard/stock_analysis_wizard_view.xml',
    ],

    'installable': True,
    'auto_install': False,
    'application': True,
}

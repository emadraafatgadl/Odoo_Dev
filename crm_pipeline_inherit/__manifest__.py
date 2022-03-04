# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'crm',
    'version': '1.3',
    'description': """
Student inherit
===================================================
""",
    'depends': ['base','crm'],
    'data': [
        'views/pipeline_sequence_view.xml',
        'security/ir.model.access.csv',
        'data/pipeline_sequence.xml',
    ],
    'test': [],
    'installable': True,
  
 
}

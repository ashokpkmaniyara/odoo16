# -*- coding: utf-8 -*-
{
    'name': "Automated Purchase Order",
    'version': '16.0.1.0.0',
    'depends': ['base','purchase'],
    'author': "Ashokpk",
    'category': 'Category',
    'description': """
    Description text
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_order_view.xml',
        'views/wizard_view.xml',
    ],
}

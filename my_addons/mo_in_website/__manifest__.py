# -*- coding: utf-8 -*-
{
    'name': "MO in Website",
    'version': '16.0.1.0.0',
    'depends': ['base','sale','website','mrp'],
    'author': "Ashokpk",
    'category': 'Category',
    'description': """
    Manufactuing orders in website
    """,
    'installable': True,
    'application': True,
    # data files always loaded at installation
    'data': [
        'views/customer_mo_view.xml',
        'views/portal_template.xml',
    ],
}

# -*- coding: utf-8 -*-
{
    'name': "Commission Plan",
    'version': '16.0.1.0.0',
    'depends': ['base','sale'],
    'author': "Ashokpk",
    'category': 'Category',
    'description': """
    Description text
    """,
    'installable': True,
    'application': True,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/crm_commission_view.xml',
        'views/sales_team_view.xml',
        'views/sales_person_view.xml',
        'views/sales_commission_view.xml',
    ],
}

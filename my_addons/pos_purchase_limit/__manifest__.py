# -*- coding: utf-8 -*-
{
    'name': "Purchase Limit",
    'version': '16.0.1.0.0',
    'depends': ['point_of_sale'],
    'author': "Ashokpk",
    'category': 'POS',
    'description': """
    Purchase limit in Pos
    """,
    'installable': True,
    'application': True,
    # data files always loaded at installation
    'data': [
        'views/purchase_limit_view.xml',
    ],
    'assets': {
        'point_of_sale.assets':[
            'pos_purchase_limit/static/src/js/limit.js',
            'pos_purchase_limit/static/src/xml/purchase_limit_template.xml'
        ],
    }
}

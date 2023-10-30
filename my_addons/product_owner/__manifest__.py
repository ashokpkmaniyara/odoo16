# -*- coding: utf-8 -*-
{
    'name': "Product Owner",
    'version': '16.0.1.0.0',
    'depends': ['point_of_sale','product'],
    'author': "Ashokpk",
    'category': 'Category',
    'description': """
    showing product owner in line and receipt
    """,
    # data files always loaded at installation
    'data': [
        'views/product_owner_view.xml',
    ],
    'assets': {
            'point_of_sale.assets': [
                'product_owner/static/src/xml/pos_receipt.xml',
                'product_owner/static/src/js/pos_receipt.js',
                'product_owner/static/src/xml/pos_order_line.xml'
            ],
    },
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
}

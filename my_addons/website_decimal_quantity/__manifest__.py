# -*- coding: utf-8 -*-
{
    'name': "Website Decimal Quantity",
    'version': '16.0.1.0.0',
    'depends': ['website_sale'],
    'author': "Ashokpk",
    'category': 'website',
    'description': """
    In the website shop, when the user clicks on the + or - button to adjust quantity,
     It should add or deduct .1 value from it
    """,
    'installable': True,
    'application': False,
    'data':['views/decimal_quantity_view.xml',
            'views/decimal_quantity_cart_view.xml',],
    'assets': {
        'web.assets_frontend': [
            'website_decimal_quantity/static/src/js/decimal_quantity.js',
            'website_decimal_quantity/static/src/js/website_sale.js',
        ]
    }
}

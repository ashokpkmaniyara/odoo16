# -*- coding: utf-8 -*-
{
    'name': "Clear Cart",
    'version': '16.0.1.0.0',
    'depends': ['base','sale','website'],
    'author': "Ashokpk",
    'category': 'Category',
    'description': """
    Clear cart button to clear all the products
    """,
    'installable': True,
    'application': True,
    # data files always loaded at installation
    'data': [
        'views/clear_cart_template.xml',
    ],
}

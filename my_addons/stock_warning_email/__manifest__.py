# -*- coding: utf-8 -*-
{
    'name': 'Stock warning email',
    'version': '16.0.1.0.0',
    'depends': ['stock'],
    'author': "Ashokpk",
    'category': 'inventory',
    'description': """Setup up a configuration where one can set up the threshold
                  quantity, products and warehouse. An email with the information of 
                  product, quantity, warehouse should be send to the warehouse manager.""",
    'installable': True,
    'application': False,
    'data':[
        'views/threshold_quantity_view.xml',
        'data/warning_email_scheduler.xml',
        'data/email_template.xml'
    ],
}

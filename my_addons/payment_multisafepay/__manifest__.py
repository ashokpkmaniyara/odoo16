{
    'name': "Multisafepay",
    'version': '16.0.1.0.0',
    'depends': ['payment','website'],
    'author': "Ashokpk",
    'category': 'ecommerse',
    'description': """
    payment gateway
    """,
    'installable': True,
    'application': True,
    # data files always loaded at installation
    'data': [
        'views/payment_provider_template.xml',
        'views/payment_provider_view.xml',
        'data/payment_provider_data.xml'
    ],

}

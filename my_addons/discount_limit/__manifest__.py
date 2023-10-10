{
    'name': "Discount Limit",
    'version': '1.0',
    'depends': ['base','sale'],
    'author': "Ashok",
    'category': 'Category',
    'description': """
    Description text
    """,
    # data files always loaded at installation
    'data': [
        'views/max_discount_limit_view.xml',
        'views/total_discount_view.xml'
    ],
    # # data files containing optionally loaded demonstration data
    # 'demo': [
    #     'views/estate_property_views.xml',
    # ],
}
{
    'name': "app123",
    'version': '1.0',
    'depends': ['base','mail','sale'],
    'author': "Ashokpk",
    'category': 'Category',
    'description': """
    Description text
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'data/service_data.xml',
        'data/type_data.xml',
        'data/sequence.xml',
        'data/scheduler.xml',
        'views/management_view.xml',
        'views/type_view.xml',
        'views/service_view.xml',
        'views/catering_view.xml',
        'views/menu_view.xml',
        'views/menu_item.xml',

    ],
    # # data files containing optionally loaded demonstration data
    # 'demo': [
    #     'views/estate_property_views.xml',
    # ],
}
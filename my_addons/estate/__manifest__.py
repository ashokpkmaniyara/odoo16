{
    'name': "estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Author Name",
    'category': 'Category',
    'description': """
    Description text
    """,
    "assets" : {
        "web.assets_backend":[
            # 'estate/static/src/js/test.js',
            # 'estate/static/src/xml/test.xml'
        ]
    },
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_view.xml',
    ],
    # # data files containing optionally loaded demonstration data
    # 'demo': [
    #     'views/estate_property_views.xml',
    # ],
}
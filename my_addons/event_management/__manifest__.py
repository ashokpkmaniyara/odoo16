# -*- coding: utf-8 -*-
{
    'name': "Event Management",
    'version': '16.0.1.0.0',
    'depends': ['base', 'mail','sale','website'],
    'author': "Ashok P K",
    'category': 'Category',
    'description': """
    Description text
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'data/event_services_default_view.xml',
        'data/event_type_default_view.xml',
        'data/catering_types_default.xml',
        'data/event_catering_sequence.xml',
        'data/event_catering_scheduler.xml',
        'data/booking_menu.xml',
        'views/event_type_view.xml',
        'views/event_booking_view.xml',
        'views/event_catering_view.xml',
        'views/event_services_view.xml',
        'views/event_catering_type_view.xml',
        'views/event_management_action.xml',
        'views/invoice_view.xml',
        'views/booking_template.xml',
        'views/customer_template.xml',
        'views/booking_snippet.xml',
        'views/booking_details_template.xml',
        'wizard/wizard.xml',
        'report/pdf_report_template.xml',
        'report/report.xml',
    ],
    'installable': True,
    'assets': {
        'web.assets_backend': [
            'event_management/static/src/js/action_manager.js',
        ],
        'web.assets_frontend': [
            'event_management/static/src/xml/dynamic_courosel.xml',
            'event_management/static/src/js/snippet.js',
            'event_management/static/src/js/booking.js',

        ]
    }
}

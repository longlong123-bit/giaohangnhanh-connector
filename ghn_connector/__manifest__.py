{
    'name': 'Giao Hang Nhanh (GHN) Connector',
    'version': '16.0.1.0',
    'summary': 'Connect Odoo Application with Giao Hang Nhanh Carrier.',
    'description': """
        The Odoo Giao Hang Nhanh (GHN) Connector module is an integrated product between the odoo application and the carrier Giao Hang Nhanh. 
        The application provides features, which through the api to manipulate directly into the dashboard of Giao Hang Nhanh.
    """,
    'category': 'Sales/Connector',
    'support': 'odoo.tangerine@gmail.com',
    'author': 'Tangerine',
    'license': 'OPL-1',
    'depends': [
        'base',
        'mail',
        'sale',
        'sale_management',
        'product',
        'stock',
        'delivery',
        'contacts'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_config_parameter.xml',
        'data/api_connect_config_data.xml',
        # 'data/api_endpoints_config_data.xml',
        'data/ghn_require_note_data.xml',
        'data/delivery_carrier_data.xml',
        'data/ghn_status_data.xml',
        'data/ghn_bin_packer_data.xml',
        'wizard/create_store_wizard_views.xml',
        # 'wizard/print_waybill_wizard.xml',
        'views/api_connect_config_views.xml',
        'views/api_connect_history_views.xml',
        'views/api_endpoint_config_views.xml',
        'views/ghn_province_views.xml',
        'views/ghn_district_views.xml',
        'views/ghn_ward_views.xml',
        'views/ghn_service_views.xml',
        'views/ghn_store_views.xml',
        'views/ghn_office_views.xml',
        'views/ghn_bin_packer_views.xml',
        'views/sale_order_views.xml',
        'views/product_template_views.xml',
        'views/delivery_carrier_views.xml',
        'views/ghn_require_note_views.xml',
        'views/ghn_status_views.xml',
        'views/res_partner_views.xml',
        # 'views/stock_picking_views.xml',
        'views/menus.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'ghn_connector/static/src/**/*.js',
            'ghn_connector/static/src/**/*.xml'
        ]
    },
    # 'external_dependencies': {
    #     'python': ['selenium']
    # },
    'images': ['static/description/thumbnail.png'],
    'application': True,
    'currency': 'USD',
    'price': '62.00'
}
{
    'name': 'Real Estate Advertisement',
    'version': '1.0',
    'summary': 'Manage real estate advertisements',
    'author': 'viba',
    'depends': ['base'],
    'data': [
        'security/security.xml',  # Include security file
        'security/ir.model.access.csv', 
        'views/estate_property_views.xml',  # Load views first
        'views/estate_menus.xml',  # Load menus after views
    ],
    'installable': True,
    'application': True,  # This makes it an 'App'
    'auto_install': False,
}

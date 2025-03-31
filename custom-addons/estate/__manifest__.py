{
    'name': 'Real Estate Advertisments',
    'version': '1.0',
    'summary': 'Post Ads for real estate.',
    'author': 'DSB',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml'
    ],
    'sequence': 5,
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}

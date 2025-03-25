{
    'name': 'Student Management',
    'version': '1.0',
    'category': 'Education',
    'summary': 'Manage student details, parents, and classes.',
    'author': 'Odoo Mates',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/student_view.xml',
        'views/parent_view.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
}

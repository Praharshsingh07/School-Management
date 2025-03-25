{
    'name': 'Class Management',
    'version': '1.0',
    'category': 'Education',
    'summary': 'Manage school classes and sections',
    'author': 'Your Name',
    'depends': ['base','Student_Management'],
    'data': [
        'security/ir.model.access.csv',
        'views/class_view.xml',
        'views/section_view.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
}

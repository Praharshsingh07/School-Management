{
    'name': 'Timetable Management',
    'description': 'Manage school classes and sections',
    'version': '1.0',
    'category': 'Education',
    'summary': 'Manage school classes and sections',
    'author': 'Your Name',
    'depends': ['base','Student_Management','Class_Management'],
    'data': [
        'security/ir.model.access.csv',
        'views/timetable_view.xml',
    ],
    'installable': True,
    'application': True,
}

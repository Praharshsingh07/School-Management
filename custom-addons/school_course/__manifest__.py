{
    'name': 'Course & Subject Management',
    'version': '1.0',
    'summary': 'Manage courses and their subjects',
    'author': 'Your Name',
    'depends': ['base','school_teacher'],
    'data': [
        'security/ir.model.access.csv',
        'views/course_view.xml',
        'views/subject_view.xml',
    ],
    'installable': True,
    'application': True,
}

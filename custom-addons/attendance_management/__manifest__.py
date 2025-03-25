{
    'name': 'Attendance Management',
    'version': '1.0',
    'summary': 'Manage student attendance',
    'author': 'Your Name',
    'depends': ['base', 'school_teacher', 'school_course'],
    'data': [
        'security/ir.model.access.csv',
        'views/attendance_view.xml',
    ],
    'installable': True,
    'application': True,
}

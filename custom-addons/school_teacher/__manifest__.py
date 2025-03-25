{
    "name": "Teacher Management",
    "summary": "Teacher Management System",
    "description": "Teacher Management System",
    "author": "DSB",
    "category": "School",
    "version": "1.0.0",
    "depends": ["base"],
    "data": [
        'views/teacher_view.xml',
        
        'security/teacher_groups.xml',
        'security/ir.model.access.csv',
       
    ],
    "installable": True,
    "application": True,
    "auto-install": False,
    "license": "LGPL-3",
}
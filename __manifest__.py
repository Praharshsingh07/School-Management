{
    "name": "School Base",
    "summary": "School Base",
    "Author": "Praharsh",
    "version":"1.0",
    "depends": ["base", "mail", "account"],
    "data": [
        "security/school_security.xml",
        "security/record_rules.xml",
        "security/ir.model.access.csv",
        # 'views/res_users_view.xml',
        "data/demo_school_data.xml",
        "data/mail_template.xml",
        "data/ir_sequence_data.xml",
        'data/server_actions.xml',
        "views/wizard_view.xml", 
        "views/student_view.xml",
        "views/teacher_view.xml",
        "views/class_view.xml",
        "views/subject_view.xml",
        "views/new_attendance.xml",
        "views/student_invoice_view.xml",
        # "views/timetable_view.xml",
        "views/menu.xml"
        
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
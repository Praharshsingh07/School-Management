{
    "name": "School Base",
    "summary": "School Base",
    "Author": "Praharsh",
    "version":"1.0",
    "depends": ["base", "mail"],
    "data": [
        "security/school_security.xml",
        "security/record_rules.xml",
        "security/ir.model.access.csv",
        "data/mail_template.xml",
        "views/student_view.xml",
        "views/teacher_view.xml",
        "views/class_view.xml",
        "views/subject_view.xml",
        "views/attendance_view.xml",
        # "views/timetable_view.xml",
        "views/menu.xml"
        
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
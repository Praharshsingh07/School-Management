from odoo import models, fields

class SchoolTeacher(models.Model):
    _name = 'school.teacher'
    _description = 'School Teacher'
    _rec_name = 'name'  # Display teacher name in dropdowns

    name = fields.Char(string='Full Name', required=True)
    employee_id = fields.Char(string='Employee ID', required=True, copy=False, unique=True)
    email = fields.Char(string='Email', unique=True)
    phone = fields.Char(string='Phone')
    
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender', required=True)

    date_of_birth = fields.Date(string='Date of Birth')
    hire_date = fields.Date(string='Hire Date', default=fields.Date.today)
    salary = fields.Float(string='Salary')

    # Relations
    subject_ids = fields.Many2many('school.subject', string="Subjects Taught")
    class_ids = fields.One2many('school.class', 'teacher_id', string="Assigned Classes")

    teacher_image = fields.Binary(string='Profile Image')

    active = fields.Boolean(string="Active", default=True)  # To archive teachers

    _sql_constraints = [
        ('unique_employee_id', 'unique(employee_id)', 'Employee ID must be unique!'),
        ('unique_email', 'unique(email)', 'Email must be unique!'),
    ]

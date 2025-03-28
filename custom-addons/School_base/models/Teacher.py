from odoo import models, fields

class Teacher(models.Model):
    _name = 'school.teacher'
    _description = 'Teacher'
    _rec_name = 'name'

    name = fields.Char(string="Full Name", required=True)
    employee_id = fields.Char(string="Employee ID", required=True, unique=True)
    subject_ids = fields.Many2many('school.subject', string="Subjects")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    joining_date = fields.Date(string="Joining Date")
    active = fields.Boolean(string="Active", default=True)

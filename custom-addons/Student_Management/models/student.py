from odoo import models, fields

class Student(models.Model):
    _name = 'student.student'
    _description = 'Student'

    name = fields.Char(string="Name", required=True)
    roll_number = fields.Char(string="Roll Number", required=True, unique=True)
    date_of_birth = fields.Date(string="Date of Birth")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")
    parent_id = fields.Many2one('student.parent', string="Parent")
    class_id = fields.Many2one('school.class', string="Class")
    section_id = fields.Many2one('school.section', string="Section")
    contact_info = fields.Char(string="Contact Info")

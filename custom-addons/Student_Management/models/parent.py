from odoo import models, fields

class Parent(models.Model):
    _name = 'student.parent'
    _description = 'Student Parent'

    name = fields.Char(string="Name", required=True)
    phone = fields.Char(string="Phone Number")
    email = fields.Char(string="Email")
    student_ids = fields.One2many('student.student', 'parent_id', string="Children")

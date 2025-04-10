from odoo import models, fields# type: ignore

class Subject(models.Model):
    _name = 'school.subject'
    _description = 'Subject'
    _rec_name = 'name'

    name = fields.Char(string="Subject Name", required=True)
    subject_code = fields.Char(string="Subject Code", required=True, unique=True)
    teacher_ids = fields.Many2many('school.teacher', string="Teachers")

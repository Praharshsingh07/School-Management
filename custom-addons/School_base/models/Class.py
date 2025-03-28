from odoo import models, fields

class Class(models.Model):
    _name = 'school.class'
    _description = 'Class'
    _rec_name = 'name'

    name = fields.Char(string="Class Name", required=True)
    section = fields.Char(string="Section")
    teacher_id = fields.Many2one('school.teacher', string="Class Teacher")
    student_ids = fields.One2many('school.student', 'class_id', string="Students")
    subject_ids = fields.Many2many('school.subject', string="Subjects")

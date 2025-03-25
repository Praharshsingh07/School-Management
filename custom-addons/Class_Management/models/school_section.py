from odoo import models, fields

class SchoolSection(models.Model):
    _name = 'school.section'
    _description = 'School Section'

    name = fields.Char(string="Section Name", required=True)
    class_id = fields.Many2one('school.class', string="Class")
    student_ids = fields.One2many('student.student', 'section_id', string="Students")
    teacher_id = fields.Many2one('teacher.teacher', string="Section Teacher")

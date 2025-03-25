from odoo import models, fields

class SchoolClass(models.Model):
    _name = 'school.class'
    _description = 'School Class'

    name = fields.Char(string="Class Name", required=True)
    section_ids = fields.One2many('school.section', 'class_id', string="Sections")
    teacher_id = fields.Many2one('teacher.teacher', string="Class Teacher")


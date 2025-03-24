from odoo import models, fields

class SchoolSubject(models.Model):
    _name = 'school.subject'
    _description = 'School Subject'

    name = fields.Char(string='Subject Name', required=True)
    subject_code = fields.Char(string='Subject Code', required=True, unique=True)
    
    category = fields.Selection([
        ('mandatory', 'Mandatory'),
        ('elective', 'Elective')
    ], string='Category', required=True, default='mandatory')

    credit_hours = fields.Integer(string='Credit Hours', required=True, default=3)

    teacher_ids = fields.Many2many('school.teacher', string="Teachers")
    class_ids = fields.Many2many('school.class', string="Classes")

    _sql_constraints = [
        ('unique_subject_code', 'unique(subject_code)', 'Subject Code must be unique!'),
    ]

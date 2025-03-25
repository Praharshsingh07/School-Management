from odoo import models, fields

class Subject(models.Model):
    _name = 'school.subject'
    _description = 'School Subject'

    name = fields.Char(string='Subject Name', required=True)
    code = fields.Char(string='Subject Code', required=True)
    course_ids = fields.Many2many(
        'school.course',  # Target model
        'course_subject_rel',  # Relation table
        'subject_id',  # This model's field in the relation table
        'course_id',  # Other model's field in the relation table
        string="Courses"
    )
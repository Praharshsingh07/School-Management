from odoo import models, fields

class Course(models.Model):
    _name = 'school.course'
    _description = 'Course Management'

    name = fields.Char(string='Course Name', required=True)
    code = fields.Char(string="Course Code", required=True)  # Added this field
    duration = fields.Integer(string="Duration (in months)")
    subject_ids = fields.Many2many(
        'school.subject',  # Target model
        'course_subject_rel',  # Relation table
        'course_id',  # This model's field in the relation table
        'subject_id',  # Other model's field in the relation table
        string="Subjects"
    )
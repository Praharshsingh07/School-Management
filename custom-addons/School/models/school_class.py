from odoo import models, fields, api

class SchoolClass(models.Model):
    _name = 'school.class'
    _description = 'School Class'

    name = fields.Char(string='Class Name', compute='_compute_class_name', store=True)
    standard = fields.Selection([
        ('1', '1st Grade'),
        ('2', '2nd Grade'),
        ('3', '3rd Grade'),
        ('4', '4th Grade'),
        ('5', '5th Grade'),
        ('6', '6th Grade'),
        ('7', '7th Grade'),
        ('8', '8th Grade'),
        ('9', '9th Grade'),
        ('10', '10th Grade'),
        ('11', '11th Grade'),
        ('12', '12th Grade')
    ], string="Standard", required=True)
    
    section = fields.Selection([
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D')
    ], string="Section", required=True)

    teacher_id = fields.Many2one('school.teacher', string="Class Teacher")
    student_ids = fields.One2many('school.student', 'class_id', string="Students")
    subject_ids = fields.Many2many('school.subject', string="Subjects")
    
    strength = fields.Integer(string="Total Students", compute='_compute_strength', store=True)

    @api.depends('standard', 'section')
    def _compute_class_name(self):
        for record in self:
            record.name = f"{record.standard} - {record.section}" if record.standard and record.section else ""

    @api.depends('student_ids')
    def _compute_strength(self):
        for record in self:
            record.strength = len(record.student_ids)

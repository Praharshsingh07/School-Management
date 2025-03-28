from odoo import models, fields

class Attendance(models.Model):
    _name = 'school.attendance'
    _description = 'Attendance Record'
    student_id = fields.Many2one('school.student', string="Student", required=True)
    class_id = fields.Many2one('school.class', string="Class", required=True)
    subject_id = fields.Many2one('school.subject', string="Subject", required=True)
    teacher_id = fields.Many2one('school.teacher', string="Marked By", required=True)
    date = fields.Date(string="Date", required=True, default=fields.Date.context_today)
    status = fields.Selection([
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    ], string="Status", required=True)
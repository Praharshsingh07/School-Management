from odoo import models, fields, api

class Attendance(models.Model):
    _name = 'school.attendance'
    _description = 'Student Attendance'

    student_id = fields.Many2one('student.student', string='Student', ondelete='cascade')
    class_id = fields.Many2one('school.class', string='Class', ondelete='cascade')
    date = fields.Date(string='Date', default=fields.Date.today)
    status = fields.Selection([
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ], string='Status', required=True, default='present')

from odoo import models, fields, api# type: ignore

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

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        
        # If current user is a teacher
        teacher = self.env['school.teacher'].search([('user_id', '=', self.env.user.id)], limit=1)
        if teacher:
            defaults['teacher_id'] = teacher.id
            
        return defaults

    @api.model
    def _search(self, args, offset=0, limit=None, order=None):
        if self.env.user.has_group('School_base.group_school_student'):
            student = self.env['school.student'].search([('user_id', '=', self.env.user.id)], limit=1)
            if student:
                args = [('student_id', '=', student.id)] + (args or [])
        return super()._search(args, offset=offset, limit=limit, order=order)
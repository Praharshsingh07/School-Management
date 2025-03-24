from odoo import models, fields, api
from datetime import datetime

class SchoolAttendance(models.Model):
    _name = 'school.attendance'
    _description = 'Student Attendance'

    student_id = fields.Many2one('school.student', string="Student", required=True)
    class_id = fields.Many2one('school.class', string="Class", related='student_id.class_id', store=True)
    subject_id = fields.Many2one('school.subject', string="Subject", required=True)
    teacher_id = fields.Many2one('school.teacher', string="Marked by Teacher", required=True)

    date = fields.Date(string="Date", default=fields.Date.today, required=True)

    status = fields.Selection([
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late')
    ], string="Attendance Status", required=True, default='present')

    check_in = fields.Datetime(string="Check-in Time", default=lambda self: datetime.now())
    check_out = fields.Datetime(string="Check-out Time")

    _sql_constraints = [
        ('unique_attendance_entry', 'unique(student_id, date, subject_id)',
         'Attendance for this student, subject, and date already exists!')
    ]

    @api.onchange('status')
    def _onchange_status(self):
        """Update check-out time based on attendance status"""
        if self.status == 'present':
            self.check_out = False
        elif self.status == 'late':
            self.check_out = datetime.now()

    @api.model
    def create(self, vals):
        """Ensure check_out is handled properly on record creation"""
        if vals.get('status') == 'present':
            vals['check_out'] = False
        return super(SchoolAttendance, self).create(vals)

    def write(self, vals):
        """Ensure check_out is handled properly on record update"""
        if vals.get('status') == 'present':
            vals['check_out'] = False
        return super(SchoolAttendance, self).write(vals)

    @api.constrains('check_in', 'check_out')
    def _check_check_in_out(self):
        """Ensure check-out is not earlier than check-in"""
        for record in self:
            if record.check_out and record.check_out < record.check_in:
                raise models.ValidationError('Check-out time cannot be earlier than Check-in time!')

    @api.constrains('date')
    def _check_date(self):
        """Ensure attendance is not marked for future dates"""
        for record in self:
            if record.date > fields.Date.today():
                raise models.ValidationError('Attendance cannot be marked for future dates!')

    @api.constrains('student_id', 'date', 'subject_id')
    def _check_attendance(self):
        """Prevent duplicate attendance records"""
        for record in self:
            existing_attendance = self.search([
                ('student_id', '=', record.student_id.id),
                ('date', '=', record.date),
                ('subject_id', '=', record.subject_id.id)
            ])
            if len(existing_attendance - record) > 0:  # Exclude the current record
                raise models.ValidationError('Attendance for this student, subject, and date already exists!')

    @api.model
    def get_student_attendance(self, student_id, date_from, date_to):
        """Retrieve attendance records for a given student in a date range"""
        return self.search([
            ('student_id', '=', student_id),
            ('date', '>=', date_from),
            ('date', '<=', date_to)
        ])

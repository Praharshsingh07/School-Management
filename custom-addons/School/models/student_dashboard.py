from odoo import models, fields, api
from datetime import datetime

class StudentDashboard(models.Model):
    _name = 'school.student.dashboard'
    _description = 'Student Dashboard'

    user_id = fields.Many2one('res.users', string="User", default=lambda self: self.env.user, readonly=True)
    student_id = fields.Many2one('school.student', string="Student", compute="_compute_student", store=True, readonly=True)
    class_id = fields.Many2one('school.class', string="Class", related='student_id.class_id', store=True)
    timetable_today = fields.Many2many('school.timetable', string="Today's Timetable", compute='_compute_timetable_today', store=True)    
    attendance_today = fields.One2many('school.attendance', 'student_id', string="Today's Attendance", compute='_compute_attendance_today',store=True)
    # subject_id= self.env['school.timetable']['subject_id']

    @api.depends('user_id')
    def _compute_student(self):
        for record in self:
            record.student_id = self.env['school.student'].search([('user_id', '=', record.user_id.id)], limit=1)

    @api.depends('class_id')
    def _compute_timetable_today(self):
        today_day = datetime.today().strftime('%A').lower()  # Get today's day (e.g., "monday")
        for record in self:
            timetable_records = self.env['school.timetable'].search([
                ('class_id', '=', record.class_id.id),
                ('day_of_week', '=', today_day)
            ])
            record.timetable_today = timetable_records

    @api.depends('student_id')
    def _compute_attendance_today(self):
        today = fields.Date.today()
        for record in self:
            record.attendance_today = self.env['school.attendance'].search([
                ('student_id', '=', record.student_id.id),
                ('date', '=', today)  # Changed from 'attendance_date' to 'date'
            ])
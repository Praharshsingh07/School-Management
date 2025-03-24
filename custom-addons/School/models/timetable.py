from odoo import models, fields

class SchoolTimetable(models.Model):
    _name = 'school.timetable'
    _description = 'School Timetable'

    class_id = fields.Many2one('school.class', string="Class", required=True)
    subject_id = fields.Many2one('school.subject', string="Subject", required=True)
    teacher_id = fields.Many2one('school.teacher', string="Teacher", required=True)

    day_of_week = fields.Selection([
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday')
    ], string="Day of the Week", required=True)

    time_slot = fields.Selection([
        ('08:00-09:00', '08:00 AM - 09:00 AM'),
        ('09:00-10:00', '09:00 AM - 10:00 AM'),
        ('10:00-11:00', '10:00 AM - 11:00 AM'),
        ('11:00-12:00', '11:00 AM - 12:00 PM'),
        ('12:00-01:00', '12:00 PM - 01:00 PM'),
        ('02:00-03:00', '02:00 PM - 03:00 PM'),
        ('03:00-04:00', '03:00 PM - 04:00 PM')
    ], string="Time Slot", required=True)

    room_no = fields.Char(string="Room Number")

    _sql_constraints = [
        ('unique_timetable_entry', 'unique(class_id, day_of_week, time_slot)', 'A class can have only one subject per time slot per day!')
    ]

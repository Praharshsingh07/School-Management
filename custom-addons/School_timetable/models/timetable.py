from odoo import models, fields, api

class Timetable(models.Model):
    _name = 'school.timetable'
    _description = 'School Timetable'

    name = fields.Char(string='Timetable Name', required=True)
    class_id = fields.Many2one('school.class', string='Class', required=True)
    section_id = fields.Many2one('school.section', string='Section')
    day = fields.Selection([
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday')
    ], string='Day', required=True)
    period_ids = fields.One2many('school.timetable.period', 'timetable_id', string='Periods')
    
    def action_do_something(self):
        for record in self:
            record.name = "Something"
        return True
    

class TimetablePeriod(models.Model):
    _name = 'school.timetable.period'
    _description = 'Timetable Period'

    timetable_id = fields.Many2one('school.timetable', string='Timetable', required=True)
    start_time = fields.Float(string='Start Time', required=True)
    end_time = fields.Float(string='End Time', required=True)
    subject_id = fields.Many2one('school.subject', string='Subject', required=True)
    teacher_id = fields.Many2one('teacher.teacher', string='Teacher')
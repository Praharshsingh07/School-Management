from odoo import models, fields, api# type: ignore

class Timetable(models.Model):
    _name = 'school.timetable'
    _description = 'Class Timetable'

    class_id = fields.Many2one('school.class', string="Class", required=True)
    subject_id = fields.Many2one('school.subject', string="Subject", required=True)
    teacher_id = fields.Many2one('school.teacher', string="Teacher", required=True)
    day = fields.Selection([
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday')
    ], string="Day", required=True)
    start_time = fields.Float(string="Start Time", required=True)
    end_time = fields.Float(string="End Time", required=True)
    student_id = fields.Many2one('school.student', string="Student", compute="_compute_student", store=False, search="_search_student")
    
    @api.depends('class_id')
    def _compute_student(self):
        for record in self:
            record.student_id = False
    
    def _search_student(self, operator, value):
        return [('class_id', '=', self.env.user.student_id.class_id.id)]
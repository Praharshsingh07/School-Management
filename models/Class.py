from odoo import models, fields# type: ignore

class Class(models.Model):
    _name = 'school.class'
    _description = 'Class'
    _rec_name = 'name'

    name = fields.Char(string="Class Name", required=True)
    section = fields.Char(string="Section")
    teacher_id = fields.Many2one('school.teacher', string="Class Teacher")
    student_ids = fields.One2many('school.student', 'class_id', string="Students")
    subject_ids = fields.Many2many('school.subject', string="Subjects")

    def action_open_attendance(self):
        """Open the attendance view for this class"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'Attendance: {self.name}',
            'res_model': 'school.attendance',
            'view_mode': 'list,form',
            'domain': [('class_id', '=', self.id)],
            'context': {
                'default_class_id': self.id,
                'hide_class': True,
                'search_default_today': True
            },
            'target': 'current',
        }

    def action_mark_attendance(self):
        """Mass attendance marking wizard for this class"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'Mark Attendance: {self.name}',
            'res_model': 'school.attendance.wizard',
            'view_mode': 'form',
            'context': {
                'default_class_id': self.id,
            },
            'target': 'new',
        }
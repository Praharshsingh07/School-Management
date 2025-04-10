from odoo import models, fields, api

class StudentDeleteWizard(models.TransientModel):
    _name = 'student.delete.wizard'
    _description = 'Confirm Student Deletion'

    student_id = fields.Many2one('school.student', string='Student', readonly=True)
    student_name = fields.Char(string="Student Name", related='student_id.name', readonly=True)

    def confirm_delete(self):
        if self.student_id:
            self.student_id.unlink()
        return {'type': 'ir.actions.act_window_close'}

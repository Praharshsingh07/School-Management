from odoo import models, fields, api# type: ignore
from odoo.exceptions import UserError # type: ignore
import logging  

_logger = logging.getLogger(__name__)
class CustomStudent(models.Model):
    _inherit = 'school.student'

    attendance_percentage = fields.Float(compute='_compute_attendance')

    def create(self, vals):
        if 'name' in vals:
            vals['name'] = vals['name'].title()
        return super().create(vals)

    def write(self, vals):
        if 'name' in vals:
            vals['name'] = vals['name'].title()
        return super().write(vals)
   
    def unlink(self):
        for student in self:
            if student.active:  # Correct condition
                raise UserError("Cannot delete active students.")
        return super().unlink()

    @api.model
    def search(self, args, **kwargs):
        args.append(('active', '=', True))
        return super().search(args, **kwargs)

    def name_get(self):
        return [(student.id, f"{student.name} ({student.roll_number})") for student in self]

    def _compute_attendance(self):
        attendance_data = self.env['school.attendance'].read_group(
            [('student_id', 'in', self.ids)],
            ['student_id', 'status'],
            ['student_id', 'status']
        )

        attendance_map = {student.id: {'total': 0, 'present': 0} for student in self}

        for record in attendance_data:
            student_id = record['student_id'][0]
            if record['status'] == 'present':
                attendance_map[student_id]['present'] = record['__count']
            attendance_map[student_id]['total'] += record['__count']

        for student in self:
            data = attendance_map.get(student.id, {})
            total = data.get('total', 0)
            present = data.get('present', 0)
            student.attendance_percentage = (present / total * 100) if total > 0 else 0

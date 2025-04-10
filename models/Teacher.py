from odoo import models, fields, api# type: ignore

class Teacher(models.Model):
    _name = 'school.teacher'
    _description = 'Teacher'
    _rec_name = 'name'

    name = fields.Char(string="Full Name", required=True)
    employee_id = fields.Char(string="Employee ID", required=True, unique=True)
    subject_ids = fields.Many2many('school.subject', string="Subjects")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    joining_date = fields.Date(string="Joining Date")
    active = fields.Boolean(string="Active", default=True)
    user_id = fields.Many2one('res.users', string='Related User', ondelete='restrict')
    class_id = fields.Many2one('school.class', string="Class")
    @api.model
    def create(self, vals):
        res = super(Teacher, self).create(vals)
        if res.user_id:
            res.user_id.write({
                'groups_id': [(4, self.env.ref('School_base.group_school_teacher').id)]
            })
        return res

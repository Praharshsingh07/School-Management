from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    teacher_id = fields.One2many('school.teacher', 'user_id', string="Teacher Record")

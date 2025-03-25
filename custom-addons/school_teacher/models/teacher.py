from odoo import models, fields, api


class TeacherTeacher(models.Model):
    _name = 'teacher.teacher'
    _description = 'Teacher Information'

    name = fields.Char(string='Name')
    emp_id = fields.Char(string='Employee ID')
    gender = fields.Selection([('male','Male'),('female','Female')],string='Gender')
    phone = fields.Char(string='Phone Number')
    email = fields.Char(string='Email')
    
    subject_ids = fields.Many2many('school.subject', string='Assigned Subjects')
    salary = fields.Float(string='Salary')
    joining_date = fields.Date(string='Joining Date')
    active = fields.Boolean(string='Active', default=True)

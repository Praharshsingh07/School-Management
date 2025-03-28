from odoo import models, fields,api

class Student(models.Model):
    _name = 'school.student'
    _description = 'Student'
    _rec_name = 'name'

    name = fields.Char(string="Full Name", required=True)
    roll_no = fields.Char(string="Roll Number", required=True, unique=True)
    class_id = fields.Many2one('school.class', string="Class", required=True)
    dob = fields.Date(string="Date of Birth")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string="Gender")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    address = fields.Text(string="Address")
    active = fields.Boolean(string="Active", default=True)
    image = fields.Binary(string="Image")

    @api.model
    def get_student_class_id(self):
        """
        Returns the current logged-in student's class ID
        """
        student = self.env.user.student_id
        return student.class_id.id if student else False
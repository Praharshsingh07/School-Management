from odoo import models, fields, api

class SchoolStudent(models.Model):
    _name = 'school.student'
    _description = 'School Student'
    _rec_name = 'name'  # Display student name in dropdowns

    name = fields.Char(string='Name', required=True)
    roll_no = fields.Integer(string='Roll No', required=True)
    age = fields.Integer(string='Age', required=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender', required=True)
    student_dob = fields.Date(string='Date of Birth')
    class_id = fields.Many2one('school.class', string='Class', required=True)
    
    address = fields.Text(string='Address')
    email = fields.Char(string='Email', unique=True)
    phone = fields.Char(string='Phone')

    # Guardian Details
    guardian_name = fields.Char(string="Guardian Name", required=True)
    guardian_phone = fields.Char(string="Guardian Phone", required=True)

    admission_date = fields.Date(string="Admission Date", default=fields.Date.today)
    
    student_image = fields.Binary(string='Student Image')
    
    active = fields.Boolean(string="Active", default=True)  # To archive students

    user_id = fields.Many2one('res.users', string="User", required=True)

    _sql_constraints = [
        ('unique_roll_no', 'unique(roll_no)', 'Roll No must be unique!'),
        ('unique_email', 'unique(email)', 'Email must be unique!'),
    ]

    @api.model
    def create(self, vals):
        """Automatically assign students to the 'Student' security group"""
        student_group = self.env.ref('your_module.group_school_student', raise_if_not_found=False)
        user = self.env['res.users'].browse(vals['user_id'])
        if student_group:
            user.write({'groups_id': [(4, student_group.id)]})
        return super(SchoolStudent, self).create(vals)

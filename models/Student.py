from odoo import models, fields, api, exceptions# type: ignore
import re

class Student(models.Model):
    _name = 'school.student'
    _description = 'Student'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Full Name", required=True,tracking=True)
    roll_no = fields.Char(string="Roll Number", required=True, unique=True)
    class_id = fields.Many2one('school.class', string="Class", required=True)
    dob = fields.Date(string="Date of Birth")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string="Gender")
    email = fields.Char(string="Email", required=True)
    phone = fields.Char(string="Phone")
    address = fields.Text(string="Address")
    active = fields.Boolean(string="Active", default=True)
    image = fields.Binary(string="Image")
    user_id = fields.Many2one('res.users', string="User", readonly=True)

    _sql_constraints = [
        ('unique_email', 'unique(email)', 'Email must be unique!'),
        ('unique_roll_no', 'unique(roll_no)', 'Roll Number must be unique!')
    ]

    @api.constrains('email')
    def _check_email(self):
        for record in self:
            if record.email:
                if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", record.email):
                    raise exceptions.ValidationError("Please enter a valid email address!")

    @api.model
    def create(self, vals):
        """
        Override create method to add a user in res.users when a student is created.
        """
        if 'email' in vals and vals['email']:
            # Check for existing user
            existing_user = self.env['res.users'].search([('login', '=', vals['email'])], limit=1)
            if existing_user:
                raise exceptions.ValidationError("A user with this email already exists.")

            # Generate a temporary password
            temp_password = 'temp123'  # In production, use a secure password generator

            # Create user vals
            user_vals = {
                'name': vals.get('name'),
                'login': vals.get('email'),
                'email': vals.get('email'),
                'password': temp_password,
                'active': vals.get('active', True),
                'groups_id': [(6, 0, [
                    self.env.ref('base.group_user').id,
                    self.env.ref('School_base.group_school_student').id
                ])]
            }
            
            try:
                new_user = self.env['res.users'].with_context(no_reset_password=True).create(user_vals)
                vals['user_id'] = new_user.id
            except Exception as e:
                raise exceptions.ValidationError(f"Error creating user: {str(e)}")

        # Create student record
        student = super(Student, self).create(vals)
        
        # Send welcome email
        student._send_welcome_email()
        
        return student

    def write(self, vals):
        """
        Override write method to handle email changes
        """
        if 'email' in vals and vals['email']:
            for record in self:
                if record.user_id:
                    record.user_id.write({
                        'login': vals['email'],
                        'email': vals['email']
                    })
        return super(Student, self).write(vals)

    def unlink(self):
        """
        Override unlink method to handle user deletion
        """
        for record in self:
            if record.user_id:
                record.user_id.active = False  # Deactivate instead of delete
        return super(Student, self).unlink()

    @api.model
    def get_student_class_id(self):
        """
        Returns the current logged-in student's class ID
        """
        student = self.env['school.student'].search([('user_id', '=', self.env.user.id)], limit=1)
        return student.class_id.id if student else False

    def action_deactivate_students(self):
        """ Deactivates selected students by setting active to False. """
        for record in self:
            record.active = False
    
    def _send_welcome_email(self):
        """
        Send welcome email to new student with login credentials
        """
        template = self.env.ref('School_base.email_template_student', raise_if_not_found=False)
        
        if not template:
            return
        
        for student in self:
            template.with_context(
                {'temp_password':'temp123'}  # Pass only the temporary password in context
            ).send_mail(
                student.id,
                force_send=True,
                email_values={
                    'email_to': student.email,
                    'subject': f'Welcome {student.name}',
                }
            )
    def action_open_delete_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Confirm Delete',
            'res_model': 'student.delete.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_student_id': self.id,
            }
        }

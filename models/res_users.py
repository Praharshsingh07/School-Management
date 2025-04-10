from odoo import models, fields, api# type: ignore
from datetime import datetime
import logging  

_logger = logging.getLogger(__name__)
class ResUsers(models.Model):
    _inherit = 'res.users'

    school_role = fields.Selection([
        ('admin', 'School Administrator'),
        ('teacher', 'School Teacher'),
        ('student', 'School Student')
    ], string='School Role')

    @api.onchange('school_role')
    def _onchange_school_role(self):
        if self.school_role:
            # Remove all existing school-related groups
            groups_to_remove = [
                self.env.ref('School_base.group_school_admin').id,
                selfself.search([('school_role', '=', 'student')]).env.ref('School_base.group_school_teacher').id,
                self.env.ref('School_base.group_school_student').id,
            ]
            self.groups_id = [(3, group_id) for group_id in groups_to_remove]
            
            # Add the new group based on selection
            if self.school_role == 'admin':
                self.groups_id = [(4, self.env.ref('School_base.group_school_admin').id)]
            elif self.school_role == 'teacher':
                self.groups_id = [(4, self.env.ref('School_base.group_school_teacher').id)]
            elif self.school_role == 'student':
                self.groups_id = [(4, self.env.ref('School_base.group_school_student').id)]

    @api.model
    def _cron_send_student_emails(self):
        """
        Cron job to send emails to students every 5 minutes
        """
        # Get all users with student role
        students = self.search([('school_role', '=', 'student')])
        
        # Get the email template
        template = self.env.ref('School_base.email_template_student_notification')
        
        for student in students:
            try:
                # Send email to each student
                template.send_mail(student.id, force_send=True)
                self.env.cr.commit()  # Commit after each email to avoid losing progress if an error occurs
            except Exception as e:
                # Log any errors but continue with other students
                _logger.error(f"Failed to send email to student {student.name}: {str(e)}")
        
        return True 
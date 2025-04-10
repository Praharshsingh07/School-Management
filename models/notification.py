from odoo import models, api, _  # type: ignore
import logging  

_logger = logging.getLogger(__name__)

class SchoolNotification(models.Model):
    _name = 'school.notification'
    _description = 'School Notification Cron'

    @api.model
    def _cron_send_student_emails(self):
        """
        Cron job to send emails to students every 5 minutes
        """
        students = self.env['res.users'].search([('school_role', '=', 'student')])

        template = self.env.ref('School_base.email_template_student_notification')
        
        for student in students:
            try:
                template.send_mail(student.id, force_send=True)
                self.env.cr.commit()
            except Exception as e:
                _logger.error(f"Failed to send email to student {student.name}: {str(e)}")

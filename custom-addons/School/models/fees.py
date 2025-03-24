from odoo import models, fields, api
from datetime import date, timedelta

class SchoolFees(models.Model):
    _name = 'school.fees'
    _description = 'Student Fees Management'

    student_id = fields.Many2one('school.student', string="Student", required=True)
    class_id = fields.Many2one('school.class', string="Class", related='student_id.class_id', store=True)
    
    fees_amount = fields.Float(string="Fees Amount", required=True)
    due_date = fields.Date(string="Due Date", required=True)
    
    payment_status = fields.Selection([
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
        ('overdue', 'Overdue')
    ], string="Payment Status", default='unpaid', compute="_compute_payment_status", store=True)
    
    late_fee = fields.Float(string="Late Fee", compute="_compute_late_fee", store=True)
    total_amount_due = fields.Float(string="Total Amount Due", compute="_compute_total_amount_due", store=True)
    
    payment_window_open = fields.Boolean(string="Payment Window Open", default=False)

    _sql_constraints = [
        ('unique_fees_entry', 'unique(student_id, due_date)',
         'Fees for this student and due date already exists!')
    ]

    @api.depends('due_date', 'payment_status')
    def _compute_payment_status(self):
        """Automatically update payment status based on due date."""
        today = date.today()
        for record in self:
            if record.payment_status != 'paid':  # Do not change if already paid
                if today > record.due_date:
                    record.payment_status = 'overdue'
                else:
                    record.payment_status = 'unpaid'

    @api.depends('due_date', 'payment_status')
    def _compute_late_fee(self):
        """Calculate late fee if the payment is overdue."""
        for record in self:
            if record.payment_status == 'overdue':
                days_late = (date.today() - record.due_date).days
                record.late_fee = days_late * 10  # ₹10 fine per day
            else:
                record.late_fee = 0

    @api.depends('fees_amount', 'late_fee')
    def _compute_total_amount_due(self):
        """Calculate total amount due including late fee."""
        for record in self:
            record.total_amount_due = record.fees_amount + record.late_fee

    def mark_as_paid(self):
        """Button action to mark fees as paid."""
        for record in self:
            record.payment_status = 'paid'
            record.late_fee = 0
            record.total_amount_due = record.fees_amount

    @api.model
    def open_fees_payment_window(self):
        """Admin method to open fees payment window."""
        self.search([]).write({'payment_window_open': True})

    @api.model
    def close_fees_payment_window(self):
        """Admin method to close fees payment window."""
        self.search([]).write({'payment_window_open': False})

from odoo import models, fields, api# type: ignore
from odoo.exceptions import UserError# type: ignore

class StudentInvoice(models.Model):
    _name = 'school.student.invoice'
    _description = 'Student Invoice'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Reference', readonly=True, default='New')
    student_id = fields.Many2one('school.student', string='Student', required=True)
    class_id = fields.Many2one(related='student_id.class_id', string='Class', store=True)
    date = fields.Date(string='Date', default=fields.Date.today, required=True)
    due_date = fields.Date(string='Due Date', required=True)
    amount = fields.Float(string='Amount', required=True)
    notes = fields.Text(string='Notes')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('posted', 'Posted'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)
    invoice_id = fields.Many2one('account.move', string='Invoice Reference', readonly=True)
    
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('school.student.invoice') or 'New'
        return super(StudentInvoice, self).create(vals)

    def action_post(self):
        for record in self:
            if record.state != 'draft':
                raise UserError('Only draft invoices can be posted!')
                
            # Create invoice
            invoice_vals = {
                'partner_id': record.student_id.user_id.partner_id.id,
                'move_type': 'out_invoice',
                'invoice_date': record.date,
                'invoice_date_due': record.due_date,
                'invoice_line_ids': [(0, 0, {
                    'name': f'School Fees - {record.student_id.name}',
                    'quantity': 1,
                    'price_unit': record.amount,
                })],
            }
            
            invoice = self.env['account.move'].create(invoice_vals)
            record.write({
                'state': 'posted',
                'invoice_id': invoice.id
            })

    def action_cancel(self):
        for record in self:
            if record.state == 'paid':
                raise UserError('Cannot cancel a paid invoice!')
            record.write({'state': 'cancelled'})
            if record.invoice_id:
                record.invoice_id.button_cancel()

    def action_view_invoice(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': self.invoice_id.id,
            'context': {'create': False},
        } 
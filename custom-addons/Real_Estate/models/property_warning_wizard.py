from odoo import models, fields

class PropertyWarningWizard(models.TransientModel):
    _name = 'property.warning.wizard'
    _description = 'Property Warning Wizard'

    message = fields.Text(string="Message", readonly=True)

    def action_close(self):
        return {'type': 'ir.actions.act_window_close'}

from odoo import models, fields

class EstateOffer(models.Model):
    _name = 'real.estate.property.offer'
    _description = 'Real Estate Property Offer'
    _order = "price desc"

    price = fields.Float('Price')
    status = fields.Selection (selection=[
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending')
    ], string="Status",default='pending')
    property_id = fields.Many2one('real.estate', string='Property')
    partner_id = fields.Many2one('res.partner', string='Partner')

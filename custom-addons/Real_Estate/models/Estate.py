from odoo import models, fields,api
from odoo.exceptions import UserError
from datetime import timedelta

class Estate(models.Model):
    _name = 'real.estate'
    _description = 'Real Estate'
    _order = "id desc"

    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    post_code = fields.Char(string='Post Code')
    date_availability = fields.Date(string='Available From',copy=False, default=lambda self: fields.Date.today() + timedelta(days=90))
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(string='Selling Price',readonly=True,copy=False)
    bedrooms = fields.Integer(string='Bedrooms',default=2)
    living_area = fields.Integer(string='Living Area')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area')
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ], string='Garden Orientation')
    active = fields.Boolean(string='Active', default=True)
    status = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled')
    ], string='Status', default='new')
    property_type_id = fields.Many2one('real.estate.type', string='Property Type')
    buyer = fields.Many2one('res.partner', string='Buyer',copy=False)
    salesperson = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    tag_ids = fields.Many2many('real.estate.property.tag', string='Tags')
    offer_ids = fields.One2many('real.estate.property.offer', inverse_name='property_id', string='Offers')
    total_area = fields.Float(string='Total Area', compute='_compute_total_area')
    best_price = fields.Float(string='Best Price', compute='_compute_best_price')


    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    @api.depends('expected_price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = record.expected_price * 0.9
    
    @api.onchange('garden')
    def _onchange_garden(self):
        if not self.garden:
            self.garden_area = 10.
            self.garden_orientation = 'north'

    def action_mark_done(self):
        for record in self:
            if record.status == 'canceled':
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Property Warning',
                    'res_model': 'property.warning.wizard',
                    'view_mode': 'form',
                    'target': 'new',
                    'context': {'default_message': 'You cannot sell a canceled property.'}
                }
            else:
                record.status = 'sold'

    def action_cancel(self):
        if self.status == 'sold':
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Property Warning',
                    'res_model': 'property.warning.wizard',
                    'view_mode': 'form',
                    'target': 'new',
                    'context': {'default_message': 'You cannot cancel a sold property.'}
                }
        else:
            self.status = 'canceled'
    
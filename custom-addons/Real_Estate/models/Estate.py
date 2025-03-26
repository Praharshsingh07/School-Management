from odoo import models, fields
from datetime import timedelta

class Estate(models.Model):
    _name = 'real.estate'
    _description = 'Real Estate'

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
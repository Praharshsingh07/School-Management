from odoo import fields, models

class prop(models.Model) :
    _name = "estate.property"
    _description = "Information About Real Estate Properties"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    expected_price = fields.Float(string="Expected Price", required=True, copy=False, default=100000)
    postcode = fields.Char('Postcode')
    date_availability = fields.Date(string='Availability Date', default=fields.Date.today, copy=False)
    # expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer('Number of Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sq ft)')
    facades = fields.Integer('Number of Facades')
    garage = fields.Boolean('Has Garage')
    garden = fields.Boolean('Has Garden')
    garden_area = fields.Integer('Garden Area (sq ft)')
    garden_orientation = fields.Selection(
        [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        string='Garden Orientation'
    )
    state = fields.Selection(
        [('new', 'New'), 
         ('offer_received', 'Offer Received'), 
         ('offer_accepted', 'Offer Accepted'), 
         ('sold', 'Sold'), 
         ('cancelled', 'Cancelled')],
        string="State",
        required=True,
        copy=False,
        default='new'
    )
    active = fields.Boolean(string="Active", default=True)
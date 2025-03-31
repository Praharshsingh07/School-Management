from logging import NullHandler
from sys import exception

from odoo import models, fields, api, exceptions
from datetime import timedelta
from odoo.tools.float_utils import float_compare, float_is_zero
# from odoo18.odoo.exceptions import UserError


class RealEstate(models.Model):
    _name = "estate.property"
    _description = "A real estate advertisement module."
    _order = "id desc"

    name = fields.Char("Title",required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Available From",
                                    copy=False,
                                    default= fields.Datetime.today() + timedelta(days=90))
    expected_price = fields.Float("Expected Price",required=True)
    selling_price = fields.Float("Selling Price", readonly=True ,copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(string="Garden Orientation",selection=[('north','North'),('south','South'),('east','East'),('west','West')],help="Garden Orientation.")
    active = fields.Boolean("active",default=True)
    state = fields.Selection(string="State",selection=[('new','New'),('received','Offer Received'),('accepted','Offer Accepted'),('sold','Sold'),('cancelled','Cancelled')],default='new')
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer = fields.Many2one("res.partner",string="Buyer",copy=False)
    salesperson_id = fields.Many2one('res.users', string='Salesperson', index=True, tracking=True,
                              default= lambda self : self.env.user)
    tag_ids = fields.Many2many("estate.property.tag",string="Tags")
    offer_ids = fields.One2many(comodel_name="estate.property.offer",inverse_name="property_id")
    total_area = fields.Integer(string="Total area (sqm)",compute="_compute_total")
    best_price = fields.Integer(string="Best Offer", compute="_compute_best_offer")

    _sql_constraints = [
        ('check_expected_price', 'CHECK( expected_price >= 0 )','A property expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK( selling_price >= 0 )', 'A property selling price must be positive.')
    ]

    @api.constrains('selling_price','expected_price')
    def _check_selling_price(self):

        for record in self:
            if float_is_zero(record.selling_price, precision_rounding=0.01):
                continue

            min_acceptable_price = record.expected_price * 0.9

            if float_compare(record.selling_price, min_acceptable_price, precision_rounding=0.01) == -1:
                raise exceptions.ValidationError(
                    "Selling price cannot be lower than 90% of the expected price!"
                )



    @api.depends("offer_ids")
    def _compute_best_offer(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0)

    @api.depends("garden_area","living_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.onchange("garden")
    def _onchange_garden(self):
        print(self.id)
        print(type(self.id))
        # id = iter(self.id)
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'

    def cancelled_property(self):
        for record in self:
            if record.state == 'sold':
                raise exceptions.UserError("Already Sold.")
            else:
                record.state = 'cancelled'

    def sold_property(self):
        for record in self:
            if record.state == 'cancelled':
                raise exceptions.UserError("Can't sell Cancelled Property.")
            else:
                record.state = 'sold'

class RealEstateType(models.Model):
    _name = "estate.property.type"
    _description = "contains property types"
    _order = "sequence, name"

    name = fields.Char("Property Type" , required=True)
    sequence = fields.Integer("Sequence",default=1)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")

    property_count = fields.Integer(compute="_compute_property_count")

    @api.depends('property_ids')
    def _compute_property_count(self):
        for rec in self:
            rec.property_count = len(rec.property_ids)

    _sql_constraints = [
        ('check_unique_type', 'unique(name)', 'A property type name must be unique.'),
    ]

    def action_view_property_ids(self):

        return {
            'name': 'Related Properties',
            'type': 'ir.actions.act_window',
            'res_model': 'estate.property',
            'view_mode': 'list,form',
            'target': 'current',
            'domain': [('property_type_id', '=', self.id)],
            'context': {'default_property_type_id': self.id},
        }


class RealEstateTags(models.Model):
    _name = "estate.property.tag"
    _description = "contains property tags"
    _order = "name"

    name = fields.Char("Tag Name", required=True)
    color = fields.Integer("Color")

    _sql_constraints = [
        ('check_unique_tag', 'unique(name)', 'A property tag name must be unique.'),
    ]

class RealEstateOffer(models.Model):
    _name = "estate.property.offer"
    _description = "contains property Offers"
    _order = "price desc"

    price = fields.Float("Property Offer" )
    status = fields.Selection(selection=[('accepted','Accepted'),('pending','Pending'),('refused','Refused')], default='pending',copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer("Validity", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True
    )

    _sql_constraints = [
        ('check_offer_price', 'CHECK( price >= 0 )', 'An offer price must be strictly positive')
    ]

    def accept_offer(self):
        if self.property_id.state in ['cancelled','sold']:
            raise exceptions.UserError(f"Already Sold to {self.property_id.buyer.name}.")
        else:
            self.property_id.selling_price = self.price
            self.property_id.state = 'sold'
            self.property_id.buyer = self.partner_id
            self.status = 'accepted'

    def reject_offer(self):
        if self.property_id.state == 'sold':
            raise exceptions.UserError(f"Already Sold to {self.property_id.buyer.name}.")
        else:
            self.status = 'refused'

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):

        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.date_deadline = create_date + timedelta(days=record.validity)

    @api.depends("date_deadline")
    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days
from odoo import models, fields, api


class HotelCustomer(models.Model):
    _name = 'hotel.customer'
    _description = 'Hotel Customer'

    name = fields.Char(string='Customer Name', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')

    # Relationships
    booking_ids = fields.One2many('hotel.booking', 'customer_id', string="Bookings")
    room_ids = fields.Many2many(
        'hotel.room',
        compute='_compute_room_ids',
        string="Rooms (via Bookings)"
    )

    @api.depends('booking_ids.room_id')
    def _compute_room_ids(self):
        for customer in self:
            customer.room_ids = customer.booking_ids.mapped('room_id')
from odoo import models, fields, api

class HotelRoom(models.Model):
    _name = "hotel.room"
    _description = "Hotel Room"

    name = fields.Char(string="Room Name", required=True)
    room_type = fields.Selection([
        ('single', 'Single'),
        ('double', 'Double'),
        ('suite', 'Suite')
    ], string="Room Type", required=True)
    price = fields.Float(string="Price")
    is_available = fields.Boolean(string="Available", default=True)

    # Relationships
    booking_ids = fields.One2many('hotel.booking', 'room_id', string="Bookings")
    customer_ids = fields.Many2many(
        'hotel.customer',
        compute='_compute_customer_ids',
        string="Customers (via Bookings)"
    )

    @api.depends('booking_ids.customer_id')
    def _compute_customer_ids(self):
        for room in self:
            room.customer_ids = room.booking_ids.mapped('customer_id')
from odoo import models, fields

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

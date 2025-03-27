from odoo import models, fields

class EstateType(models.Model):
    _name = 'real.estate.type'
    _description = 'Real Estate Type'
    _order = "name"

    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer(string='Sequence')
    
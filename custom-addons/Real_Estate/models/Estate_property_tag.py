from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = 'real.estate.property.tag'
    _description = 'Real Estate Property Tag'
    _order = "name"

    name = fields.Char(string='Name', required=True)
    color = fields.Integer(string="Color")

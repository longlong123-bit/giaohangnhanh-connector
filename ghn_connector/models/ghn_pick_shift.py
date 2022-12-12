from odoo import fields, models


class GHNPickShift(models.Model):
    _name = 'ghn.pick.shift'
    _description = 'Choose a delivery time for the shipper'

    name = fields.Char(string='Title')
    from_time = fields.Integer(string='From time')
    to_time = fields.Integer(string='To time')
    sale_order_id = fields.Many2one('sale.order', string='Sale order')
from odoo import fields, models


class GHNPickShift(models.Model):
    _name = 'ghn.pick.shift'
    _description = 'Get a list delivery time of the shipper'

    name = fields.Char(string='Title')
    from_time = fields.Datetime(string='From time')
    to_time = fields.Datetime(string='To time')
    sale_order_id = fields.Many2one('sale.order', string='Sale order')

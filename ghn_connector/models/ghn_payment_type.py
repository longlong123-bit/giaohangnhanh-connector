from odoo import fields, models


class GHNPaymentType(models.Model):
    _name = 'ghn.payment.type'
    _description = 'Provider values of payment type Giao Hang Nhanh'

    name = fields.Char(string='Name')
    code = fields.Char(string='Code')

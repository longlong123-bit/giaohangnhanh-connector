from odoo import fields, models


class GHNStatus(models.Model):
    _name = 'giaohangnhanh.status'
    _inherit = ['mail.thread']
    _description = 'Giao hang nhanh Status'
    _order = 'code desc'

    vi_name = fields.Char(string='Name', required=True, readonly=True)
    en_name = fields.Char(string='Name', required=True, readonly=True)
    code = fields.Char(string='Code', required=True, readonly=True)


class GHNRequiredNote(models.Model):
    _name = 'giaohangnhanh.require.note'
    _description = 'Required note of Giao Hang Nhanh'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True, readonly=True)
    description = fields.Text(string='Description')


class GHNPaymentType(models.Model):
    _name = 'giaohangnhanh.payment.type'
    _description = 'Provider values of payment type Giao Hang Nhanh'

    name = fields.Char(string='Name')
    code = fields.Char(string='Code')

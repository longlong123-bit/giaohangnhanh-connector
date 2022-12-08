from odoo import fields, models


class GHNStatus(models.Model):
    _name = 'ghn.status'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'GHN Status'
    _order = 'code desc'

    vi_name = fields.Char(string='Name', required=True, readonly=True)
    en_name = fields.Char(string='Name', required=True, readonly=True)
    code = fields.Char(string='Code', required=True, readonly=True)

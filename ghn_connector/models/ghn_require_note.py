from odoo import fields, models


class GHNRequiredNote(models.Model):
    _name = 'ghn.require.note'
    _description = 'Required note of Giao Hang Nhanh'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True, readonly=True)
    description = fields.Text(string='Description')

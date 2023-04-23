from odoo import fields, models, api


class PartnerVTPost(models.Model):
    _inherit = 'res.partner'
    _description = 'Configuration Address Receiver'

    ghn_province_id = fields.Many2one('giaohangnhanh.province', string='Province')
    ghn_district_id = fields.Many2one('giaohangnhanh.district', string='District')
    ghn_ward_id = fields.Many2one('giaohangnhanh.ward', string='Ward')
    ghn_street = fields.Char(string='Street')

    @api.onchange('ghn_ward_id')
    def _onchange_vtp_ward_id(self):
        for rec in self:
            if rec.ghn_ward_id:
                rec.ghn_district_id = rec.ghn_ward_id.did
                rec.ghn_province_id = rec.ghn_ward_id.did.pid

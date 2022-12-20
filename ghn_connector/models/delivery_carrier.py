from odoo import fields, models


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'
    _description = 'Configuration GHN Carrier'

    ghn_store_ids = fields.One2many('ghn.store', 'delivery_carrier_id', string='Stores')
    ghn_post_office_ids = fields.One2many('ghn.post.office', 'delivery_carrier_id', string='Post Offices')
    ghn_province_ids = fields.One2many('ghn.province', 'delivery_carrier_id', string='Provinces')
    ghn_district_ids = fields.One2many('ghn.district', 'delivery_carrier_id', string='Districts')
    ghn_ward_ids = fields.One2many('ghn.ward', 'delivery_carrier_id', string='Wards')
    delivery_carrier_code = fields.Char(string='Delivery Carrier Code')

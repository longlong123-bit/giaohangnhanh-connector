from odoo import fields, models, _


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'
    _description = 'Configuration Giao Hang Nhanh Carrier'

    # ghn_store_ids = fields.One2many('ghn.store', 'delivery_carrier_id', string='Stores')
    # ghn_post_office_ids = fields.One2many('ghn.post.office', 'delivery_carrier_id', string='Post Offices')
    # ghn_province_ids = fields.One2many('giaohangnhanh.province', 'delivery_carrier_id', string='Provinces')
    # ghn_district_ids = fields.One2many('giaohangnhanh.district', 'delivery_carrier_id', string='Districts')
    # ghn_ward_ids = fields.One2many('giaohangnhanh.ward', 'delivery_carrier_id', string='Wards')
    # delivery_carrier_code = fields.Char(string='Delivery Carrier Code')

    delivery_type = fields.Selection(selection_add=[('giaohangnhanh', 'Giao Hang Nhanh')])

    @staticmethod
    def giaohangnhanh_send_shipping(pickings):
        res = []
        for p in pickings:
            res = res + [{'exact_price': p.carrier_id.fixed_price, 'tracking_number': False}]
        return res

    def giaohangnhanh_rate_shipment(self, order):
        carrier = self._match_address(order.partner_shipping_id)
        if not carrier:
            return {
                'success': False,
                'price': 0.0,
                'error_message': _('Error: this delivery method is not available for this address.'),
                'warning_message': False
            }
        price = self.fixed_price
        company = self.company_id or order.company_id or self.env.company
        if company.currency_id and company.currency_id != order.currency_id:
            price = company.currency_id._convert(price, order.currency_id, company, fields.Date.today())
        return {
            'success': True,
            'price': price,
            'error_message': False,
            'warning_message': False
        }

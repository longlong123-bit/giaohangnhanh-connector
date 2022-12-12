import base64

from odoo import fields, models, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError
from odoo.addons.ghn_connector.contanst.ghn_contanst import Const
from odoo.addons.ghn_connector.contanst.ghn_contanst import Message


class SaleOrderVTPost(models.Model):
    _inherit = 'sale.order'
    _description = 'For Giao Hang Nhanh Carrier'

    partner_id = fields.Many2one(
        'res.partner', string='Customer', readonly=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        required=True, change_default=True, index=True, tracking=1,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", )
    waybill_code = fields.Char(string='Waybill code', readonly=True)
    delivery_carrier_id = fields.Many2one('delivery.carrier', string='Delivery Method')
    ghn_store_id = fields.Many2one('ghn.store', string='Warehouse')

    sender_fullname = fields.Char(related='ghn_store_id.name', string='Fullname')
    sender_phone = fields.Char(related='ghn_store_id.phone', string='Phone')
    sender_address = fields.Char(related='ghn_store_id.address', string='Street')
    sender_province_id = fields.Many2one(related='ghn_store_id.pid', string='Province')
    sender_district_id = fields.Many2one(related='ghn_store_id.did', string='District')
    sender_ward_id = fields.Many2one(related='ghn_store_id.wid', string='Ward')
    sender_cid = fields.Integer(related='ghn_store_id.cid', string='Cid')

    receiver_fullname = fields.Char(related='partner_id.name', string='Fullname')
    receiver_phone = fields.Char(related='partner_id.mobile', string='Phone')
    receiver_email = fields.Char(related='partner_id.email', string='Email')
    receiver_street = fields.Char(related='partner_id.ghn_street', string='Street')
    receiver_ward_id = fields.Many2one(related='partner_id.ghn_ward_id', string='Ward')
    receiver_district_id = fields.Many2one(related='partner_id.ghn_district_id', string='District')
    receiver_province_id = fields.Many2one(related='partner_id.ghn_province_id', string='Province')

    ghn_note = fields.Text(string='Note')
    ghn_pick_shift_id = fields.Many2one('ghn.pick.shift', string='Pick shift')
    ghn_service_id = fields.Many2one('ghn.service', string='Service')

    def get_pick_shift(self):
        client = self.env['api.connect.config'].generate_client_api_ghn()
        res = client.get_pick_shift()
        self.env['ghn.pick.shift'].create({
            'name': res['title'],
            'from_time': int(res['from_time']),
            'to_time': int(res['to_time']),
            'sale_order_id': self.id
        })

    def get_service(self):
        client = self.env['api.connect.config'].generate_client_api_ghn()
        payload = self._prepare_payload_for_get_service()
        res = client.get_service(payload)
        self.env['ghn.service'].create({
            'service_id': int(res['service_id']),
            'short_name': res['short_name'],
            'service_type_id': int(res['service_type_id']),
            'sale_order_id': self.id
        })

    def _prepare_payload_for_get_service(self):
        payload = {
            'shop_id': self.ghn_store_id.cid,
            'from_district': self.ghn_store_id.did,
            'to_district': self.partner_id.ghn_district_id.did
        }
        return payload

    def calculate_fee(self):
        client = self.env['api.connect.config'].generate_client_api_ghn()
        payload = self._prepare_payload_for_cal_fee()
        res = client.get_service(payload)

    def calculate_total_size_and_weight(self):
        height = 0.0
        width = 0.0
        depth = 0.0
        weight = 0.0
        for line in self.order_line:
            if line.product_id.product_tmpl_id.gross_height > 150.0:
                raise UserError(_('The height of the product should not exceed 150 cm'))
            if line.product_id.product_tmpl_id.gross_width > 150.0:
                raise UserError(_('The width of the product should not exceed 150 cm'))
            if line.product_id.product_tmpl_id.gross_length > 150.0:
                raise UserError(_('The width of the product should not exceed 150 cm'))
            height += line.product_id.product_tmpl_id.gross_height * line.product_uom_qty
            width += line.product_id.product_tmpl_id.gross_width * line.product_uom_qty
            depth += line.product_id.product_tmpl_id.gross_depth * line.product_uom_qty
            weight += (height * width * depth) / 5000
        weight *= 1000
        if round(weight) > 30000:
            raise UserError(_('The total weight of the product should not exceed 30 kg'))
        return weight
    # def _prepare_payload_for_cal_fee(self):
    #     payload = {
    #         'from_district_id': self.ghn_store_id.did,
    #         'service_id': self.ghn_service_id.service_id,
    #         'service_type_id': self.ghn_service_id.service_type_id,
    #         'to_district_id': self.ghn_store_id.did,
    #         'to_ward_code': self.ghn_store_id.wid.code,
    #         'height': self.,
    #         'length': ,
    #         'weight': ,
    #         'width': ,
    #         'insurance_value':10000,
    #         'coupon': null
    #     }
    #     return payload

    # def action_create_waybill_code(self):
    #     try:
    #         client = self.env['api.connect.config'].generate_client_api_ghn()
    #         payload = self._prepare_data_create_waybill()
    #         res = client.create_waybill(payload)
    #         self.env['sale.order.line'].create({
    #             'product_id': self.delivery_carrier_vtp_id.product_id.id,
    #             'name': f'{self.vtp_lst_service_id.display_name}\n{self.vtp_lst_extent_service_id.display_name}'
    #             if self.vtp_lst_extent_service_id else f'{self.vtp_lst_service_id.display_name}',
    #             'product_uom_qty': 1.0,
    #             'price_unit': res['MONEY_TOTAL'],
    #             'price_subtotal': res['MONEY_TOTAL'],
    #             'price_total': res['MONEY_TOTAL'],
    #             'sequence': self.order_line[-1].sequence + 1,
    #             'order_id': self.order_line[-1].order_id.id,
    #             'is_delivery': True
    #         })
    #         self.write({
    #             'waybill_code': res['ORDER_NUMBER'],
    #             'money_collection': res['MONEY_COLLECTION'],
    #             'money_total': res['MONEY_TOTAL'],
    #             'money_total_fee': res['MONEY_TOTAL_FEE'],
    #             'money_fee': res['MONEY_FEE'],
    #             'money_collection_fee': res['MONEY_COLLECTION_FEE'],
    #             'money_vat': res['MONEY_VAT'],
    #             'actual_kpi_ht': f"{int(res['KPI_HT'])} giờ",
    #             'exchange_weight': res['EXCHANGE_WEIGHT'],
    #             'money_other_fee': res['MONEY_OTHER_FEE'],
    #         })
    #     except Exception as e:
    #         raise UserError(_(f'Create waybill failed. {e}'))

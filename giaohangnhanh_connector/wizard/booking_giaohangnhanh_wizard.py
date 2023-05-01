from typing import Dict
from odoo import models, fields, _, api
from odoo.tools import ustr
from odoo.exceptions import UserError

from odoo.addons.giaohangnhanh_connector.dataclass.giaohangnhanh_order import Order


class BookingGiaohangnhanhWizard(models.TransientModel):
    _name = 'booking.giaohangnhanh.wizard'
    _description = 'This module fills and confirms info about shipment before creating a bill of lading Giao Hang Nhanh'

    @staticmethod
    def _compute_weight_for_product(item):
        return ((item.product_id.gross_length * item.product_id.gross_height * item.product_id.gross_width) / 6000.0) * item.product_uom_qty

    @staticmethod
    def _get_items(order_line) -> (list, float):
        total_amount = 0.0
        items = []
        for item in order_line:
            if not item.is_delivery:
                total_amount += item.price_total
                items.append((0, 0,
                    {
                        'product_id': item.product_id.id,
                        'name': item.name,
                        'quantity': item.product_uom_qty,
                        'price': item.price_total,
                        'weight': BookingGiaohangnhanhWizard._compute_weight_for_product(item)
                    }))
        return items, total_amount

    @api.model
    def default_get(self, fields_list):
        values = super(BookingGiaohangnhanhWizard, self).default_get(fields_list)
        if values.get('deli_order_id'):
            deli_order_id = self.env['stock.picking'].browse(values.get('deli_order_id'))
            if deli_order_id:
                items, total_amount = BookingGiaohangnhanhWizard._get_items(deli_order_id.sale_id.order_line)
                values.update({
                    'client_order_code': deli_order_id.sale_id.name,
                    'insurance_value': total_amount,
                    'item_ids': items
                })
        return values

    def _get_default_payment_type(self):
        payment_type_id = self.env.ref('giaohangnhanh_connector.ghn_payment_type_1')
        if payment_type_id:
            return payment_type_id.id

    def _get_default_required_note(self):
        require_note_id = self.env.ref('giaohangnhanh_connector.ghn_require_note_2')
        if require_note_id:
            return require_note_id.id

    carrier_id = fields.Many2one('delivery.carrier', string='Delivery Carrier', required=True, readonly=True)
    deli_order_id = fields.Many2one('stock.picking', string='Delivery order', required=True, readonly=True)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)

    receiver_id = fields.Many2one('res.partner', string='Receiver', required=True)
    receiver_phone = fields.Char(related='receiver_id.phone', string='Phone')
    receiver_street = fields.Char(related='receiver_id.ghn_street', string='Street')
    receiver_ward_id = fields.Many2one(related='receiver_id.ghn_ward_id', string='Ward')
    receiver_district_id = fields.Many2one(related='receiver_id.ghn_district_id', string='District')
    receiver_province_id = fields.Many2one(related='receiver_id.ghn_province_id', string='Province')

    sender_id = fields.Many2one('giaohangnhanh.store', string='Store', required=True)
    sender_name = fields.Char(related='sender_id.name', string='Sender')
    sender_phone = fields.Char(related='sender_id.phone', string='Phone')
    sender_address = fields.Char(related='sender_id.address', string='Address')
    sender_province_id = fields.Many2one(related='sender_id.pid', string='Province')
    sender_district_id = fields.Many2one(related='sender_id.did', string='District')
    sender_ward_id = fields.Many2one(related='sender_id.wid', string='Ward')

    length = fields.Float(string='Length', required=True, help='Maximum 150 cm')
    weight = fields.Float(string='Weight', required=True, help='Maximum 30 kg')
    width = fields.Float(string='Width', required=True, help='Maximum 150 cm')
    height = fields.Float(string='Height', required=True, help='Maximum 150 cm')

    service_id = fields.Many2one('giaohangnhanh.service', string='Service')
    payment_type_id = fields.Many2one('giaohangnhanh.payment.type', string='Payment Type', required=True,
                                      default=_get_default_payment_type)
    required_note_id = fields.Many2one('giaohangnhanh.require.note', string='Require Note', required=True,
                                       default=_get_default_required_note)
    item_ids = fields.One2many('booking.giaohangnhanh.line.wizard', 'shipment_id', string='Shipment line item')
    cod_amount = fields.Monetary(string='COD', currency_field='currency_id', help='Maximum 10.000.000đ')
    is_required = fields.Boolean(help='The field is used set attribute for field service_id', default=False)
    coupon = fields.Char(string='Coupon')
    client_order_code = fields.Char(string='Order Code')

    insurance_value = fields.Monetary(string='Insurance Value', help='Maximum 5.000.000đ')
    note = fields.Text(string='Note')

    @api.onchange('height', 'length', 'width')
    def _onchange_compute_weight(self):
        for rec in self:
            if rec.height or rec.length or rec.width:
                rec.weight = ((rec.height * rec.length * rec.width) / 6000.0) * 1000.0

    def _get_payload_get_service(self) -> Dict[str, int]:
        payload: Dict[str, int] = {
            'shop_id': self.sender_id.cid,
            'from_district': self.sender_id.did.did,
            'to_district': self.receiver_id.ghn_district_id.did
        }
        return payload

    def action_get_service_for_shipment(self):
        try:
            client = self.env['api.connect.instances'].generate_ghn_client_api()
            payload = self._get_payload_get_service()
            lst_service_need_create: list = []
            dataset = client.get_list_service(payload)
            if dataset:
                service_ids = [rec.get('service_id') for rec in dataset]
                lst_data_services = self.env['giaohangnhanh.service'].search(
                    [('service_id', 'in', service_ids)])
                lst_service_existed = [rec.service_id for rec in lst_data_services]
                for data in dataset:
                    if data.get('service_id') not in lst_service_existed:
                        lst_service_need_create.append({
                            'service_id': data.get('service_id'),
                            'name': data.get('short_name'),
                            'service_type_id': data.get('service_type_id')
                        })
                if lst_service_need_create:
                    self.env['giaohangnhanh.service'].create(lst_service_need_create)
                return {
                    'name': _('Giao Hang Nhanh Shipment Information'),
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_model': self._name,
                    'res_id': self.id,
                    'target': 'new',
                    'context': {
                        'service_supported': service_ids,
                        'default_service_id': lst_data_services[0].id,
                        'default_is_required': True
                    }
                }
        except Exception as e:
            raise UserError(ustr(e))

    def _validate_payload(self):
        payload_fields = {
            'Delivery carrier': self.carrier_id,
            'Delivery order': self.deli_order_id,
            'Sender': self.sender_id,
            'Sender Phone': self.sender_phone,
            'Sender Name': self.sender_name,
            'Sender Street': self.sender_address,
            'Sender Ward': self.sender_ward_id,
            'Sender District': self.sender_district_id,
            'Sender Province': self.sender_province_id,
            'Service Type': self.service_id,
            'Product Type': self.payment_type_id,
            'Required Note': self.required_note_id,
            'Receiver': self.receiver_id,
            'Receiver Phone': self.receiver_phone,
            'Receiver Street': self.receiver_street,
            'Receiver Ward': self.receiver_ward_id,
            'Receiver District': self.receiver_district_id,
            'Receiver Province': self.receiver_province_id,
            'List Item': len(self.deli_order_id.sale_id.order_line)
        }
        for field, value in payload_fields.items():
            if not value:
                raise UserError(_(f'The field {field} is required.'))

    def action_booking_giaohangnhanh(self):
        try:
            self._validate_payload()
            client = self.env['api.connect.instances'].generate_ghn_client_api()
            payload = Order.parser_class_shipment(self)
            result = client.create_waybill(payload)
            dataclass_order = Order(*Order.parser_dict(result))
            payload_shipment = Order.parser_class_order_shipment(dataclass_order, self)
            payload_do = Order.parser_class_do(dataclass_order, carrier_id=self.carrier_id.id)
            line_data_ship_fee = Order.parser_class_order_line(self, dataclass_order.total_fee)
            self.env['giaohangnhanh.shipment'].create(payload_shipment)
            self.deli_order_id.write(payload_do)
            self.env['sale.order.line'].create(line_data_ship_fee)
        except Exception as e:
            raise UserError(_(ustr(e)))


class BookingGiaohangnhanhLineWizard(models.TransientModel):
    _name = 'booking.giaohangnhanh.line.wizard'

    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    shipment_id = fields.Many2one('booking.giaohangnhanh.wizard')
    name = fields.Char(string='Name', required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float(string='Quantity', required=True)
    price = fields.Monetary(string='Price', currency_field='currency_id', required=True)
    weight = fields.Float(string='Weight')

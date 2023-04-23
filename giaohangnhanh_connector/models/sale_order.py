import base64

from odoo import fields, models, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError
from odoo.addons.giaohangnhanh_connector.constants.ghn_constants import Const, Message


class SaleOrderVTPost(models.Model):
    _inherit = 'sale.order'
    _description = 'For Giao Hang Nhanh Carrier'

    def _default_required_note(self):
        require_note_id = self.env['ghn.require.note'].search([('code', '=', Const.REQUIRE_NOTE_DEFAULT)])
        if require_note_id:
            return require_note_id

    def _default_payment_type(self):
        payment_type_id = self.env['ghn.payment.type'].search([('code', '=', Const.PAYMENT_TYPE_DEFAULT)])
        if payment_type_id:
            return payment_type_id

    partner_id = fields.Many2one(
        'res.partner', string='Customer', readonly=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        required=True, change_default=True, index=True, tracking=1,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", )
    waybill_code = fields.Char(string='Waybill code', readonly=True)
    delivery_carrier_id = fields.Many2one('delivery.carrier', string='Delivery Method')
    ghn_store_id = fields.Many2one('ghn.store', string='Store')

    sender_fullname = fields.Char(related='ghn_store_id.name', string='Fullname')
    sender_phone = fields.Char(related='ghn_store_id.phone', string='Phone')
    sender_address = fields.Char(related='ghn_store_id.address', string='Street')
    sender_province_id = fields.Many2one(related='ghn_store_id.pid', string='Province')
    sender_district_id = fields.Many2one(related='ghn_store_id.did', string='District')
    sender_ward_id = fields.Many2one(related='ghn_store_id.wid', string='Ward')

    receiver_fullname = fields.Char(related='partner_id.name', string='Fullname')
    receiver_phone = fields.Char(related='partner_id.mobile', string='Phone')
    receiver_email = fields.Char(related='partner_id.email', string='Email')
    receiver_street = fields.Char(related='partner_id.ghn_street', string='Street')
    receiver_ward_id = fields.Many2one(related='partner_id.ghn_ward_id', string='Ward')
    receiver_district_id = fields.Many2one(related='partner_id.ghn_district_id', string='District')
    receiver_province_id = fields.Many2one(related='partner_id.ghn_province_id', string='Province')

    ghn_note = fields.Text(string='Note')
    ghn_require_note = fields.Many2one('ghn.require.note', string='Require Note', default=_default_required_note)
    ghn_pick_shift_id = fields.Many2one('ghn.pick.shift', string='Choose pick shift')
    ghn_service_id = fields.Many2one('ghn.service', string='Service')
    ghn_bin_packer_ids = fields.One2many('ghn.bin.packer.sale.order', 'sale_order_id')
    ghn_payment_type_id = fields.Many2one('ghn.payment.type', string='Payment type', default=_default_payment_type)
    ghn_cod_amount = fields.Monetary(string='COD amount')
    ghn_pickup_time = fields.Datetime(string='Pickup time')
    is_get_service = fields.Boolean(default=False)
    is_get_pick_shift = fields.Boolean(default=False)
    ghn_content = fields.Text(string='Content')
    ghn_post_office_id = fields.Many2one('ghn.post.office', string='Send goods at post office')
    total_fee = fields.Monetary(string='Total fee', readonly=True)
    expected_delivery_time = fields.Char(string='Expected delivery time', readonly=True)

    def get_list_pick_shift(self):
        client = self.env['api.connect.instances'].generate_client_api_ghn()
        res = client.get_list_pick_shift()
        for rec in res:
            self.env['ghn.pick.shift'].create({
                'name': rec['title'],
                'from_time': datetime.fromtimestamp(rec['from_time']),
                'to_time': datetime.fromtimestamp(rec['to_time']),
                'sale_order_id': self.id
            })
        self.write({'is_get_pick_shift': True})
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Get list pick shift successfully!"),
                "type": "success",
                "message": _(Message.MSG_ACTION_SUCCESS),
                "sticky": False,
                "next": {"type": "ir.actions.act_window_close"},
            },
        }

    def get_list_service(self):
        client = self.env['api.connect.instances'].generate_client_api_ghn()
        payload = self._prepare_payload_for_get_service()
        res = client.get_list_service(payload)
        for rec in res:
            ghn_service_id = self.env['ghn.service'].search([('service_id', '=', rec['service_id']),
                                                             ('sale_order_id', '=', self.id)])
            if not ghn_service_id:
                ghn_service_id.create({
                    'service_id': int(rec['service_id']),
                    'name': rec['short_name'],
                    'service_type_id': int(rec['service_type_id']),
                    'sale_order_id': self.id
                })
        self.write({'is_get_service': True})
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Get list services successfully!"),
                "type": "success",
                "message": _(Message.MSG_ACTION_SUCCESS),
                "sticky": False,
                "next": {"type": "ir.actions.act_window_close"},
            },
        }

    def _prepare_payload_for_get_service(self):
        if not self.ghn_store_id:
            raise UserError(_('The field store is required.'))
        payload = {
            'shop_id': self.ghn_store_id.cid,
            'from_district': self.ghn_store_id.did.did,
            'to_district': self.partner_id.ghn_district_id.did
        }
        return payload

    def calculate_fee(self):
        client = self.env['api.connect.instances'].generate_client_api_ghn()
        payload = self._prepare_payload_for_cal_fee()
        res = client.get_service(payload)

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

    def _building_items(self) -> (list, int):
        lines = []
        insurance_value = 0
        if not len(self.order_line):
            raise UserError(_('The order lines not found.'))
        for item in self.order_line:
            line = {
                'name': item.product_id.product_tmpl_id.name,
                'quantity': int(item.product_uom_qty),
                'price': int(item.price_subtotal),
                'height': int(item.product_id.product_tmpl_id.gross_height),
                'width': int(item.product_id.product_tmpl_id.gross_width),
                'length': int(item.product_id.product_tmpl_id.gross_length)
            }
            insurance_value += int(item.price_subtotal)
            lines.append(line)
        if insurance_value > Const.MAXIMUM_INSURANCE_VALUE:
            raise UserError(_('The maximum insurance value is 5,000,000đ.'))
        return lines, insurance_value

    def _compute_bin_packer(self) -> (int, int, int, int):
        depth = 0
        width = 0
        height = 0
        weight = 0
        for bin in self.ghn_bin_packer_ids:
            depth += int(bin.depth)
            width += int(bin.width)
            height += int(bin.height)
            weight += int(bin.vol_weight)
        if depth > Const.MAXIMUM_DEPTH_SIZE_PACKER:
            raise UserError(_('The maximum depth is 150 cm.'))
        elif width > Const.MAXIMUM_WIDTH_SIZE_PACKER:
            raise UserError(_('The maximum width is 150 cm.'))
        elif height > Const.MAXIMUM_HEIGHT_SIZE_PACKER:
            raise UserError(_('The maximum height is 150 cm.'))
        elif weight > Const.MAXIMUM_WEIGHT_SIZE_PACKER:
            raise UserError(_('The maximum weight is 30 kg.'))

        return weight, width, height, depth

    def _prepare_data_create_waybill(self) -> dict:
        if not self.ghn_store_id:
            raise UserError(_('The field store is required.'))
        elif not self.partner_id:
            raise UserError(_('The field partner is required.'))
        elif not len(self.ghn_bin_packer_ids):
            raise UserError(_('The field bin packer is required.'))
        elif not self.ghn_service_id:
            raise UserError(_('The field service is required.'))
        elif not self.ghn_payment_type_id:
            raise UserError(_('The field payment type is required.'))
        elif not self.ghn_require_note:
            raise UserError(_('The field require note is required.'))
        elif self.ghn_cod_amount > Const.MAXIMUM_COD_VALUE:
            raise UserError(_('The maximum code value is 10,000,000đ.'))
        lines, insurance_value = self._building_items()
        weight, width, height, depth = self._compute_bin_packer()
        payload = {
            'payment_type_id': int(self.ghn_payment_type_id.code),
            'note': self.ghn_note or '',
            'shop_id': self.ghn_store_id.cid,
            'from_name': self.ghn_store_id.name,
            'from_phone': self.ghn_store_id.phone,
            'from_address': self.ghn_store_id.address,
            'from_ward_name': self.ghn_store_id.wid.name,
            'from_district_name': self.ghn_store_id.did.name,
            'from_province_name': self.ghn_store_id.pid.name,
            'required_note': self.ghn_require_note.code,
            'to_name': self.partner_id.name,
            'to_phone': self.partner_id.mobile,
            'to_address': self.partner_id.ghn_street,
            'to_ward_name': self.partner_id.ghn_ward_id.name,
            'to_district_name': self.partner_id.ghn_district_id.name,
            'to_province_name': self.partner_id.ghn_province_id.name,
            'cod_amount': int(self.ghn_cod_amount),
            'content': self.ghn_content or '',
            'weight': weight,
            'length': depth,
            'width': width,
            'height': height,
            'pick_station_id': self.ghn_post_office_id.office_id,
            'insurance_value': insurance_value,
            'service_id': self.ghn_service_id.service_id,
            'service_type_id': self.ghn_service_id.service_type_id,
            # 'pick_shift': [self.ghn_pick_shift_id.name],
            # 'pickup_time': int(round(self.ghn_pickup_time.timestamp())) if self.ghn_pickup_time else 0,
            'client_order_code': self.name,
            'items': lines
        }
        return payload

    def action_create_waybill_code(self):
        try:
            client = self.env['api.connect.instances'].generate_client_api_ghn()
            payload = self._prepare_data_create_waybill()
            res = client.create_waybill(payload)
            self.env['sale.order.line'].create({
                'product_id': self.delivery_carrier_id.product_id.id,
                'name': f'{self.ghn_service_id.display_name}',
                'product_uom_qty': 1.0,
                'price_unit': res['total_fee'],
                'price_subtotal': res['total_fee'],
                'price_total': res['total_fee'],
                'sequence': self.order_line[-1].sequence + 1,
                'order_id': self.order_line[-1].order_id.id,
                'is_delivery': True
            })
            self.write({
                'waybill_code': res['order_code'],
                'total_fee': res['total_fee'],
                'expected_delivery_time': res['expected_delivery_time']
            })
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": _("Get list services successfully!"),
                    "type": "success",
                    "message": _(Message.MSG_ACTION_SUCCESS),
                    "sticky": False,
                    "next": {"type": "ir.actions.act_window_close"},
                },
            }
        except Exception as e:
            raise UserError(_(f'Create waybill failed. {e}'))

    def action_cancel(self):
        res = super(SaleOrderVTPost, self).action_cancel()
        if self.waybill_code:
            client = self.env['api.connect.instances'].generate_client_api_ghn()
            payload = {
                'order_codes': [self.waybill_code]
            }
            client.cancel_order(payload)
        return res

    def action_find_bin_packer(self):
        """
            Hệ thống sẽ tự động tính toán và đưa ra gợi ý size thùng sao cho:
            - Thùng hàng sẽ chứa được hết tất cả các sản phẩm.
            - Thùng hàng sẽ có kích thước nhỏ nhất.
        """
        bin_fit = []
        packer = Packer()
        bin_packers = self.env['ghn.bin.packer'].search([])
        for bin in bin_packers:
            packer.add_bin(Bin(bin.name, bin.width, bin.height, bin.depth, bin.vol_weight))
        for line in self.order_line:
            product = line.product_id.product_tmpl_id
            if line.product_id.product_tmpl_id.is_auto_compute_weight:
                volumetric_weight = product.weight
            else:
                volumetric_weight = product.gross_width * product.gross_height * product.gross_length / 5000 * 1000
            packer.add_item(
                Item(product.name, product.gross_width, product.gross_height, product.gross_length, volumetric_weight, product.id))
        packer.pack()
        lst_good_suggest_bin = [bin for bin in packer.bins if not len(bin.unfitted_items)]
        if len(lst_good_suggest_bin) > 0:
            bin_fit.append(min(lst_good_suggest_bin, key=lambda b: b.get_volume()))
        else:
            raise UserError(_('Can not make a bin packer suggestion in the list of available bin packer. '
                              'Please add a new bin packer'))
        for b in bin_fit:
            bin_packer_id = self.env['ghn.bin.packer.sale.order'].search([('name', '=', b.name), ('sale_order_id', '=', self.id)])
            if not bin_packer_id:
                self.env['ghn.bin.packer.sale.order'].create({
                    'name': b.name,
                    'width': b.width,
                    'height': b.height,
                    'depth': b.depth,
                    'sale_order_id': self.id,
                    'volume': b.get_volume(),
                    'product_ids': [(6, 0, [item.id for item in b.items])]
                })
            else:
                raise UserError(_(f'The bin packer {b.name} existed.'))


class GHNBinPackerSaleOrder(models.Model):
    _name = 'ghn.bin.packer.sale.order'
    _inherit = 'ghn.bin.packer'
    _description = 'Bin packer for sale order'

    sale_order_id = fields.Many2one('sale.order', string='Sale order')
    product_ids = fields.Many2many('product.template', string='Product')

    def action_save_bin_packer(self):
        bin_packer_id = self.env['ghn.bin.packer'].search([('name', '=', self.name)])
        if not bin_packer_id:
            bin_packer_id.create({
                'name': self.name,
                'width': self.width,
                'height': self.height,
                'depth': self.depth
            })
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": _("Save information bin packer successfully!"),
                    "type": "success",
                    "message": _(Message.MSG_ACTION_SUCCESS),
                    "sticky": False,
                    "next": {"type": "ir.actions.act_window_close"},
                },
            }
        else:
            raise UserError(_(f'The bin packer {self.name} existed.'))

from odoo import fields, models, _
from odoo.exceptions import UserError
from odoo.addons.giaohangnhanh_connector.constants.ghn_constants import Const


class GHNShipment(models.Model):
    _name = 'giaohangnhanh.shipment'
    _inherit = ['mail.thread']
    _rec_name = 'carrier_tracking_ref'
    _description = 'This module is used to store data about the shipment Giao Hang Nhanh'

    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    delivery_order_id = fields.Many2one('stock.picking', string='Delivery Order', required=True)
    carrier_id = fields.Many2one('delivery.carrier', string='Carrier', required=True,
                                 default=lambda self: self.env['delivery.carrier'].search([('delivery_type', '=', 'giaohangnhanh')]).id)
    carrier_tracking_ref = fields.Char(string='Carrier Tracking Ref', required=True)
    carrier_tracking_link = fields.Char(string='Carrier Tracking Link', compute='_compute_carrier_tracking_url')
    total_fee = fields.Monetary(string='Total Fee', required=True, currency_field='currency_id', tracking=True)
    insurance_value = fields.Monetary(string='Insurance Value', required=True)
    trans_type = fields.Char(string='Trans Type')
    expected_delivery_time = fields.Datetime(string='Expected Deli Time')
    state = fields.Char(string='State', required=True, tracking=True)
    sort_code = fields.Char(string='Sort Code', required=True)
    note = fields.Text(string='Note')

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

    length = fields.Float(string='Length', required=True)
    weight = fields.Float(string='Weight', required=True, tracking=True)
    width = fields.Float(string='Width', required=True)
    height = fields.Float(string='Height', required=True)

    service_id = fields.Many2one('giaohangnhanh.service', string='Service')
    payment_type_id = fields.Many2one('giaohangnhanh.payment.type', string='Payment Type', required=True)
    required_note_id = fields.Many2one('giaohangnhanh.require.note', string='Require Note', required=True)
    item_ids = fields.One2many('giaohangnhanh.shipment.line', 'shipment_id', string='Shipment line')
    coupon = fields.Char(string='Coupon')
    client_order_code = fields.Char(string='Client Order Code')
    cod_amount = fields.Monetary(string='COD', currency_field='currency_id')

    def _compute_cm_uom_name(self):
        self.cm_uom_name = self.env['product.template']._get_cm_uom_name_from_ir_config_parameter()

    def _compute_vol_weight_uom_name(self):
        self.vol_weight_uom_name = self.env['product.template']._get_vol_weight_uom_name_from_ir_config_parameter()

    cm_uom_name = fields.Char(string='Height unit of measure label', compute='_compute_cm_uom_name')
    vol_weight_uom_name = fields.Char(string='Volumetric weight unit of measure label',
                                      compute='_compute_vol_weight_uom_name')

    def _compute_carrier_tracking_url(self):
        for rec in self:
            rec.carrier_tracking_link = Const.TRACKING_LINK.format(bl_code=rec.carrier_tracking_ref)

    def open_website_url(self):
        self.ensure_one()
        if not self.carrier_tracking_link:
            raise UserError(_("Your delivery method has no redirect on courier provider's website to track this order."))
        return {
            'type': 'ir.actions.act_url',
            'name': "Shipment Tracking Page",
            'target': 'new',
            'url': self.carrier_tracking_link,
        }

    def action_update_shipment(self):
        ...

    def action_print_shipment_info(self):
        ...

    def action_cancel_shipment(self):
        ...


class GiaohangnhanhShipmentLine(models.Model):
    _name = 'giaohangnhanh.shipment.line'

    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    shipment_id = fields.Many2one('giaohangnhanh.shipment')
    name = fields.Char(string='Name', required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float(string='Quantity', required=True)
    price = fields.Monetary(string='Price', currency_field='currency_id', required=True)
    weight = fields.Float(string='Weight')

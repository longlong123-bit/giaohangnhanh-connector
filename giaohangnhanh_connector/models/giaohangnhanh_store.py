from odoo import fields, api, models, _
from odoo.exceptions import UserError

from odoo.addons.giaohangnhanh_connector.constants.ghn_constants import Const, Message


class ViettelPostStore(models.Model):
    _name = 'giaohangnhanh.store'
    _inherit = ['mail.thread']
    _description = 'Giao Hang Nhanh Store'

    cid = fields.Integer(string='Customer Id', required=True, readonly=True)
    name = fields.Char(string='Name', required=True, tracking=True)
    phone = fields.Char(string='Phone', required=True, tracking=True)
    address = fields.Char(string='Address', required=True, tracking=True)
    pid = fields.Many2one('giaohangnhanh.province', string='Province', required=True, tracking=True)
    did = fields.Many2one('giaohangnhanh.district', string='District', required=True, tracking=True)
    wid = fields.Many2one('giaohangnhanh.ward', string='Ward', required=True, tracking=True)
    clid = fields.Integer(string='Client Id', readonly=True)
    version_no = fields.Char(string='Version No', readonly=True)

    @api.model
    def sync_stores(self):
        client = self.env['api.connect.instances'].generate_client_api_ghn()
        try:
            delivery_carrier_id = self.env['delivery.carrier'].search(
                [('delivery_carrier_code', '=', Const.DELIVERY_CARRIER_CODE)])
            if not delivery_carrier_id:
                raise UserError(_(Message.MSG_NOT_CARRIER))
            dataset = client.sync_stores()
            if len(dataset['shops']) > 0:
                for data in dataset['shops']:
                    cid = self.search([('cid', '=', data['_id'])])
                    district_id = self.env['giaohangnhanh.district'].search([('did', '=', data['district_id'])])
                    ward_id = self.env['giaohangnhanh.ward'].search([('code', '=', data['ward_code'])])
                    payload = {
                        'cid': data['_id'],
                        'name': data['name'],
                        'phone': data['phone'],
                        'address': data['address'],
                        'pid': district_id.pid.id,
                        'did': district_id.id,
                        'wid': ward_id.id,
                        'clid': data['client_id'],
                        'status': str(data['status']),
                        'version_no': data['version_no'],
                        'delivery_carrier_id': delivery_carrier_id.id
                    }
                    if not cid:
                        self.create(payload)
                    else:
                        cid.write(payload)
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": _("Sync stores successfully!"),
                    "type": "success",
                    "message": _(Message.MSG_ACTION_SUCCESS),
                    "sticky": False,
                    "next": {"type": "ir.actions.act_window_close"},
                },
            }
        except Exception as e:
            raise UserError(_(f'Sync Store failed. Error: {str(e)}'))

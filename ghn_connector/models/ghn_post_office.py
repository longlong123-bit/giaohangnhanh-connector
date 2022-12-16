from odoo import fields, api, models, _
from odoo.exceptions import UserError

from odoo.addons.ghn_connector.constants.ghn_constants import Const
from odoo.addons.ghn_connector.constants.ghn_constants import Message


class GHNPostOffice(models.Model):
    _name = 'ghn.post.office'
    _description = 'List Giao Hang Nhanh Post Office'

    name = fields.Char(string='Post office name')
    code = fields.Char(string='Code')
    office_id = fields.Integer(string='Location ID')
    email = fields.Char(string='Email')
    province_name = fields.Char(string='Province name')
    district_name = fields.Char(string='District name')
    ward_name = fields.Char(string='Ward name')
    address = fields.Char(string='Address')
    latitude = fields.Char(string='Latitude')
    longitude = fields.Char(string='Longitude')
    iframe_map = fields.Html(string='Iframe map')
    delivery_carrier_id = fields.Many2one('delivery.carrier', string='Delivery Carrier')

    @api.model
    def sync_offices(self):
        try:
            client = self.env['api.connect.config'].generate_client_api_ghn()
            delivery_carrier_id = self.env['delivery.carrier'].search(
                [('delivery_carrier_code', '=', Const.DELIVERY_CARRIER_CODE)])
            if not delivery_carrier_id:
                raise UserError(_(Message.MSG_NOT_CARRIER))
            dataset = client.sync_offices()
            if len(dataset) > 0:
                for data in dataset:
                    office_id = self.search([('office_id', '=', data['locationId'])])
                    dict_office = {
                        'name': data['locationName'],
                        'code': data['locationCode'],
                        'province_name': data['provinceName'],
                        'district_name': data['districtName'],
                        'ward_name': data['wardName'],
                        'address': data['address'],
                        'latitude': data['latitude'],
                        'longitude': data['longitude'],
                        'email': data['email'],
                        'iframe_map': data['iframeMap'],
                        'office_id': data['locationId'],
                        'delivery_carrier_id': delivery_carrier_id.id
                    }
                    if not office_id:
                        self.create(dict_office)
                    else:
                        office_id.write(dict_office)
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": _("Sync post office successfully!"),
                    "type": "success",
                    "message": _(Message.MSG_ACTION_SUCCESS),
                    "sticky": False,
                    "next": {"type": "ir.actions.act_window_close"},
                },
            }
        except Exception as e:
            raise UserError(_(f'Sync office failed. Error: {str(e)}'))

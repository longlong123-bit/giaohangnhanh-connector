from odoo import fields, api, models, _
from odoo.exceptions import UserError

from odoo.addons.viettelpost_connector.clients.viettelpost_clients import ViettelPostClient
from odoo.addons.viettelpost_connector.contanst.viettelpost_contanst import Const
from odoo.addons.viettelpost_connector.contanst.viettelpost_contanst import Message


class GHNService(models.Model):
    _name = 'ghn.service'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'List GHN Service'

    name = fields.Char(string='Name')
    code = fields.Integer(string='Code')
    type = fields.Integer(string='Type')
    delivery_carrier_id = fields.Many2one('delivery.carrier', string='Delivery Carrier')

    # @api.model
    # def sync_service(self):
    #     server_id = self.env['api.connect.config'].search([('code', '=', Const.BASE_CODE), ('active', '=', True)])
    #     if not server_id:
    #         raise UserError(_(Message.BASE_MSG))
    #     client = ViettelPostClient(server_id.host, server_id.token, self)
    #     try:
    #         delivery_carrier_id = self.env['delivery.carrier'].search(
    #             [('delivery_carrier_code', '=', Const.DELIVERY_CARRIER_CODE)])
    #         if not delivery_carrier_id:
    #             raise UserError(_(Message.MSG_NOT_CARRIER))
    #         payload = {'TYPE': Const.TYPE_SERVICE}
    #         dataset = client.get_services(payload)
    #         if len(dataset) > 0:
    #             for data in dataset:
    #                 service_id = self.search([('code', '=', data['SERVICE_CODE'])])
    #                 dict_service = {
    #                     'name': data['SERVICE_NAME'],
    #                     'code': data['SERVICE_CODE'],
    #                     'delivery_carrier_id': delivery_carrier_id.id
    #                 }
    #                 if not service_id:
    #                     self.create(dict_service)
    #                 else:
    #                     service_id.write(dict_service)
    #         return {
    #             "type": "ir.actions.client",
    #             "tag": "display_notification",
    #             "params": {
    #                 "title": _("Sync Service Successfully!"),
    #                 "type": "success",
    #                 "message": _(Message.MSG_ACTION_SUCCESS),
    #                 "sticky": False,
    #                 "next": {"type": "ir.actions.act_window_close"},
    #             },
    #         }
    #     except Exception as e:
    #         raise UserError(_(f'Sync service failed. Error: {str(e)}'))

    @api.depends('name', 'code')
    def name_get(self):
        res = []
        for record in self:
            name = record.name
            if record.code:
                name = f'[{record.code}] - {name}'
            res.append((record.id, name))
        return res

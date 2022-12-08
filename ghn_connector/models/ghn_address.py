from odoo import fields, models, _, api
from odoo.exceptions import UserError

from odoo.addons.viettelpost_connector.clients.viettelpost_clients import GHNClient
from odoo.addons.viettelpost_connector.contanst.viettelpost_contanst import Const
from odoo.addons.viettelpost_connector.contanst.viettelpost_contanst import Message


class GHNProvince(models.Model):
    _name = 'ghn.province'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Giao Hang Nhanh Provinces'

    def _default_country(self):
        return self.env['res.country'].search([('code', '=', 'VN')]).id

    delivery_carrier_id = fields.Many2one('delivery.carrier', string='Delivery Carrier')
    country_id = fields.Many2one('res.country', string='Country', required=True, tracking=True, default=_default_country)
    pid = fields.Integer(string='ID', required=True, tracking=True)
    code = fields.Char(string='Code', required=True, tracking=True)
    name = fields.Char(string='Name', required=True, tracking=True)
    name_extend = fields.Text(string='Extension Name', tracking=True)
    active = fields.Boolean(string='Active', tracking=True)
    can_update_cod = fields.Boolean(string='Can Update COD', tracking=True)
    status = fields.Selection([('1', 'Unlock'), ('2', 'Lock')], string='Status', tracking=True)
    district_ids = fields.One2many('ghn.district', 'pid', string='Districts')

    # @api.model
    # def sync_province(self):
    #     server_id = self.env['api.connect.config'].search([('code', '=', Const.BASE_CODE), ('active', '=', True)])
    #     if not server_id:
    #         raise UserError(_(Message.BASE_MSG))
    #     client = GHNClient(server_id.host, server_id.token, self)
    #     try:
    #         delivery_carrier_id = self.env['delivery.carrier'].search(
    #             [('delivery_carrier_code', '=', Const.DELIVERY_CARRIER_CODE)])
    #         if not delivery_carrier_id:
    #             raise UserError(_(Message.MSG_NOT_CARRIER))
    #         dataset = client.sync_provinces()
    #         if len(dataset) > 0:
    #             for data in dataset:
    #                 province_id = self.search([('pid', '=', data['ProvinceID'])])
    #                 payload = {
    #                     'pid': data['ProvinceID'],
    #                     'name': data['ProvinceName'],
    #                     'code': data['Code'],
    #                     'name_extend': ', '.join(data['NameExtension']),
    #                     'active': True if data['IsEnable'] == 1 else False,
    #                     'delivery_carrier_id': delivery_carrier_id.id
    #                 }
    #                 if not province_id:
    #                     self.create(payload)
    #                 else:
    #                     province_id.write({
    #                         'name': data['ProvinceName'],
    #                         'name_extend': ', '.join(data['NameExtension']),
    #                         'active': True if data['IsEnable'] == 1 else False
    #                     })
    #         return {
    #             "type": "ir.actions.client",
    #             "tag": "display_notification",
    #             "params": {
    #                 "title": _("Sync Provinces Successfully!"),
    #                 "type": "success",
    #                 "message": _(Message.MSG_ACTION_SUCCESS),
    #                 "sticky": False,
    #                 "next": {"type": "ir.actions.act_window_close"},
    #             },
    #         }
    #     except Exception as e:
    #         raise UserError(_(f'Sync province failed. Error: {str(e)}'))


class GHNDistrict(models.Model):
    _name = 'ghn.district'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Giao Hang Nhanh Districts'

    delivery_carrier_id = fields.Many2one('delivery.carrier', string='Delivery Carrier')
    did = fields.Integer(string='Id', required=True, tracking=True)
    pid = fields.Many2one('ghn.province', string='Province ID', required=True, tracking=True)
    name = fields.Char(string='Name', required=True, tracking=True)
    support_type = fields.Selection([
        ('0', 'Lock'),
        ('1', 'Take/Pay'),
        ('2', 'Deliver'),
        ('3', 'Take/Deliver/Pay')], string='Support Type', tracking=True)
    status = fields.Selection([('1', 'Unlock'), ('2', 'Lock')], string='Status', tracking=True)
    name_extend = fields.Text(string='Extension Name', tracking=True)
    can_update_cod = fields.Boolean(string='Can update COD')
    ward_ids = fields.One2many('ghn.ward', 'did', string='Wards')

    # @api.model
    # def sync_district(self):
    #     server = self.env['api.connect.config'].search([('code', '=', Const.BASE_CODE), ('active', '=', True)])
    #     if not server:
    #         raise UserError(_(Message.BASE_MSG))
    #     client = ViettelPostClient(server.host, server.token, self)
    #     try:
    #         delivery_carrier_id = self.env['delivery.carrier'].search(
    #             [('delivery_carrier_code', '=', Const.DELIVERY_CARRIER_CODE)])
    #         if not delivery_carrier_id:
    #             raise UserError(_(Message.MSG_NOT_CARRIER))
    #         dataset = client.get_districts()
    #         if len(dataset) > 0:
    #             for data in dataset:
    #                 province_id = self.env['ghn.country.province'].search([('province_id', '=', data['PROVINCE_ID'])])
    #                 if not province_id:
    #                     continue
    #                 district_id = self.search([('district_id', '=', data['DISTRICT_ID'])])
    #                 if not district_id:
    #                     self.create({
    #                         'district_id': data['DISTRICT_ID'],
    #                         'district_code': data['DISTRICT_VALUE'],
    #                         'district_name': data['DISTRICT_NAME'].title(),
    #                         'province_id': province_id.id,
    #                         'delivery_carrier_id': delivery_carrier_id.id
    #                     })
    #                 else:
    #                     district_id.write({
    #                         'district_code': data['DISTRICT_VALUE'],
    #                         'district_name': data['DISTRICT_NAME'].title()
    #                     })
    #         return {
    #             "type": "ir.actions.client",
    #             "tag": "display_notification",
    #             "params": {
    #                 "title": _("Sync District Successfully!"),
    #                 "type": "success",
    #                 "message": _(Message.MSG_ACTION_SUCCESS),
    #                 "sticky": False,
    #                 "next": {"type": "ir.actions.act_window_close"},
    #             },
    #         }
    #     except Exception as e:
    #         raise UserError(_(f'Sync district failed. Error: {str(e)}'))


class GHNWard(models.Model):
    _name = 'ghn.ward'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Giao Hang Nhanh Wards'

    delivery_carrier_id = fields.Many2one('delivery.carrier', string='Delivery Carrier')
    name = fields.Char(string='Ward Name', required=True, tracking=True)
    code = fields.Char(string='Code', required=True, tracking=True)
    did = fields.Many2one('ghn.district', string='District', required=True, tracking=True)
    name_extend = fields.Text(string='Extension Name', tracking=True)
    active = fields.Boolean(string='Active')
    can_update_cod = fields.Char(string='Can update COD')
    support_type = fields.Selection([
        ('0', 'Lock'),
        ('1', 'Take/Pay'),
        ('2', 'Deliver'),
        ('3', 'Take/Deliver/Pay')], string='Support Type', tracking=True)
    status = fields.Selection([('1', 'Unlock'), ('2', 'Lock')], string='Status', tracking=True)

    # @api.model
    # def sync_ward(self):
    #     server = self.env['api.connect.config'].search([('code', '=', Const.BASE_CODE), ('active', '=', True)])
    #     if not server:
    #         raise UserError(_(Message.BASE_MSG))
    #     client = ViettelPostClient(server.host, server.token, self)
    #     try:
    #         delivery_carrier_id = self.env['delivery.carrier'].search(
    #             [('delivery_carrier_code', '=', Const.DELIVERY_CARRIER_CODE)])
    #         if not delivery_carrier_id:
    #             raise UserError(_(Message.MSG_NOT_CARRIER))
    #         dataset = client.get_wards()
    #         if len(dataset) > 0:
    #             for data in dataset:
    #                 district_id = self.env['ghn.country.district'].search([('district_id', '=', data['DISTRICT_ID'])])
    #                 if not district_id:
    #                     continue
    #                 ward_id = self.search([('ward_id', '=', data['WARDS_ID'])])
    #                 if not ward_id:
    #                     self.create({
    #                         'ward_id': data['WARDS_ID'],
    #                         'ward_name': data['WARDS_NAME'].title(),
    #                         'district_id': district_id.id,
    #                         'delivery_carrier_id': delivery_carrier_id.id
    #                     })
    #                 else:
    #                     ward_id.write({'ward_name': data['WARDS_NAME'].title()})
    #         return {
    #             "type": "ir.actions.client",
    #             "tag": "display_notification",
    #             "params": {
    #                 "title": _("Sync District Successfully!"),
    #                 "type": "success",
    #                 "message": _(Message.MSG_ACTION_SUCCESS),
    #                 "sticky": False,
    #                 "next": {"type": "ir.actions.act_window_close"},
    #             },
    #         }
    #     except Exception as e:
    #         raise UserError(_(f'Sync ward failed. Error: {str(e)}'))
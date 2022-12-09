from odoo import fields, models, _, api
from odoo.exceptions import UserError

from odoo.addons.ghn_connector.contanst.ghn_contanst import Const
from odoo.addons.ghn_connector.contanst.ghn_contanst import Message
from odoo.addons.ghn_connector.api_conf.ghn_client import GHNClient


class GHNProvince(models.Model):
    _name = 'ghn.province'
    _order = 'pid asc'
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

    @api.model
    def sync_provinces(self):
        client = self.env['api.connect.config'].generate_client_api_ghn()
        try:
            delivery_carrier_id = self.env['delivery.carrier'].search(
                [('delivery_carrier_code', '=', Const.DELIVERY_CARRIER_CODE)])
            if not delivery_carrier_id:
                raise UserError(_(Message.MSG_NOT_CARRIER))
            dataset = client.sync_provinces()
            if len(dataset) > 0:
                for data in dataset:
                    province_id = self.search([('pid', '=', data['ProvinceID'])])
                    payload = {
                        'pid': data['ProvinceID'],
                        'name': data['ProvinceName'],
                        'code': data['Code'],
                        'active': True if data['IsEnable'] == 1 else False,
                        'status': str(data['Status']),
                        'can_update_cod': data['CanUpdateCOD'],
                        'delivery_carrier_id': delivery_carrier_id.id
                    }
                    if 'NameExtension' in data:
                        payload.update({'name_extend': '\n'.join(data['NameExtension']) if len(
                            data['NameExtension']) > 0 else '', })

                    if not province_id:
                        self.create(payload)
                    else:
                        province_id.write(payload)
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": _("Sync provinces successfully!"),
                    "type": "success",
                    "message": _(Message.MSG_ACTION_SUCCESS),
                    "sticky": False,
                    "next": {"type": "ir.actions.act_window_close"},
                },
            }
        except Exception as e:
            raise UserError(_(f'Sync province failed. Error: {str(e)}'))


class GHNDistrict(models.Model):
    _name = 'ghn.district'
    _order = 'did asc'
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

    @api.model
    def sync_districts(self):
        client = self.env['api.connect.config'].generate_client_api_ghn()
        try:
            delivery_carrier_id = self.env['delivery.carrier'].search(
                [('delivery_carrier_code', '=', Const.DELIVERY_CARRIER_CODE)])
            if not delivery_carrier_id:
                raise UserError(_(Message.MSG_NOT_CARRIER))
            dataset = client.sync_districts()
            if len(dataset) > 0:
                for data in dataset:
                    province_id = self.env['ghn.province'].search([('pid', '=', data['ProvinceID'])])
                    if not province_id:
                        raise UserError(_(f'The province id {data["ProvinceID"]} not found.'))
                    district_id = self.search([('did', '=', data['DistrictID'])])
                    payload = {
                        'did': data['DistrictID'],
                        'support_type': str(data['SupportType']),
                        'name': data['DistrictName'],
                        'pid': province_id.id,
                        'status': str(data['Status']),
                        'can_update_cod': data['CanUpdateCOD'],
                        'delivery_carrier_id': delivery_carrier_id.id
                    }
                    if 'NameExtension' in data:
                        payload.update({'name_extend': '\n'.join(data['NameExtension']) if len(data['NameExtension']) > 0 else '',})
                    if not district_id:
                        self.create(payload)
                    else:
                        district_id.write(payload)
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": _("Sync District successfully!"),
                    "type": "success",
                    "message": _(Message.MSG_ACTION_SUCCESS),
                    "sticky": False,
                    "next": {"type": "ir.actions.act_window_close"},
                },
            }
        except Exception as e:
            raise UserError(_(f'Sync district failed. Error: {str(e)}'))


class GHNWard(models.Model):
    _name = 'ghn.ward'
    _order = 'did asc'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Giao Hang Nhanh Wards'

    delivery_carrier_id = fields.Many2one('delivery.carrier', string='Delivery Carrier')
    name = fields.Char(string='Ward Name', required=True, tracking=True)
    code = fields.Char(string='Code', required=True, tracking=True)
    did = fields.Many2one('ghn.district', string='District', required=True, tracking=True)
    name_extend = fields.Text(string='Extension Name', tracking=True)
    can_update_cod = fields.Char(string='Can update COD')
    support_type = fields.Selection([
        ('0', 'Lock'),
        ('1', 'Take/Pay'),
        ('2', 'Deliver'),
        ('3', 'Take/Deliver/Pay')], string='Support Type', tracking=True)
    status = fields.Selection([('1', 'Unlock'), ('2', 'Lock')], string='Status', tracking=True)

    @api.model
    def sync_wards(self):
        client = self.env['api.connect.config'].generate_client_api_ghn()
        try:
            delivery_carrier_id = self.env['delivery.carrier'].search(
                [('delivery_carrier_code', '=', Const.DELIVERY_CARRIER_CODE)])
            if not delivery_carrier_id:
                raise UserError(_(Message.MSG_NOT_CARRIER))
            dataset = client.sync_wards()
            if len(dataset) > 0:
                for data in dataset:
                    district_id = self.env['ghn.district'].search([('did', '=', data['DistrictID'])])
                    if not district_id:
                        continue
                        # raise UserError(_(f'The district id {data["DistrictID"]} not found.'))
                    ward_id = self.search([('code', '=', data['WardCode'])])
                    payload = {
                        'code': data['WardCode'],
                        'name': data['WardName'],
                        'did': district_id.id,
                        'support_type': str(data['SupportType']),
                        'status': str(data['Status']),
                        'can_update_cod': data['CanUpdateCOD'],
                        'delivery_carrier_id': delivery_carrier_id.id
                    }
                    if 'NameExtension' in data:
                        payload.update({'name_extend': '\n'.join(data['NameExtension']) if len(
                            data['NameExtension']) > 0 else '', })
                    if not ward_id:
                        self.create(payload)
                    else:
                        ward_id.write(payload)
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": _("Sync wards successfully!"),
                    "type": "success",
                    "message": _(Message.MSG_ACTION_SUCCESS),
                    "sticky": False,
                    "next": {"type": "ir.actions.act_window_close"},
                },
            }
        except Exception as e:
            raise UserError(_(f'Sync wards failed. Error: {str(e)}'))

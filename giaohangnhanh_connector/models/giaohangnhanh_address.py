from typing import List
from odoo import fields, models, _, api
from odoo.exceptions import UserError
from odoo.addons.giaohangnhanh_connector.dataclass.giaohangnhanh_address import Province, District, Ward
from odoo.addons.api_connect_instances.common.action import Action
from odoo.addons.giaohangnhanh_connector.constants.ghn_constants import Const, Message


class GHNProvince(models.Model):
    _name = 'giaohangnhanh.province'
    _order = 'pid asc'
    _inherit = ['mail.thread']
    _description = 'Giao Hang Nhanh Provinces'

    def _default_country(self):
        return self.env['res.country'].search([('code', '=', 'VN')]).id

    cid = fields.Many2one('res.country', string='Country', required=True, tracking=True, default=_default_country)
    pid = fields.Integer(string='ID', required=True, tracking=True)
    code = fields.Char(string='Code', required=True, tracking=True)
    name = fields.Char(string='Name', required=True, tracking=True)
    active = fields.Boolean(string='Active', tracking=True)
    district_ids = fields.One2many('giaohangnhanh.district', 'pid', string='Districts')

    @api.model
    def sync_provinces(self):
        try:
            client = self.env['api.connect.instances'].generate_ghn_client_api()
            dataset = client.sync_provinces()
            if dataset:
                lst_province_need_create: list = []
                dataclass_province: List[Province] = [Province(*Province.parser_dict(rec)) for rec in dataset]
                lst_pid: List[int] = [rec.id for rec in dataclass_province]
                lst_exists_province: List[GHNProvince] = self.search([('pid', 'in', lst_pid)])
                lst_exists_province_ids: List[int] = [rec.pid for rec in lst_exists_province]
                for data in dataclass_province:
                    if data.id not in lst_exists_province_ids:
                        lst_province_need_create.append(Province.parser_class(data))
                if lst_province_need_create:
                    self.create(lst_province_need_create)
            return Action.display_notification(_('Sync provinces successfully!'), _(Message.MSG_ACTION_SUCCESS))
        except Exception as e:
            raise UserError(_(f'Sync provinces failed. Error: {str(e)}'))


class GHNDistrict(models.Model):
    _name = 'giaohangnhanh.district'
    _order = 'did asc'
    _inherit = ['mail.thread']
    _description = 'Giao Hang Nhanh Districts'

    did = fields.Integer(string='Id', required=True, tracking=True)
    pid = fields.Many2one('giaohangnhanh.province', string='Province ID', required=True, tracking=True)
    name = fields.Char(string='Name', required=True, tracking=True)
    code = fields.Char(string='code', tracking=True)
    ward_ids = fields.One2many('giaohangnhanh.ward', 'did', string='Wards')
    active = fields.Boolean(string='Active')

    @api.model
    def sync_districts(self):
        try:
            client = self.env['api.connect.instances'].generate_ghn_client_api()
            dataset = client.sync_districts()
            if dataset:
                lst_district_need_create: list = []
                dataclass_district: List[District] = [District(*District.parser_dict(rec)) for rec in dataset]
                lst_did: List[int] = [rec.id for rec in dataclass_district]
                lst_exists_district: List[GHNDistrict] = self.search([('did', 'in', lst_did)])
                lst_exists_district_ids: List[int] = [rec.did for rec in lst_exists_district]
                for data in dataclass_district:
                    if data.id not in lst_exists_district_ids:
                        province_id = self.env['giaohangnhanh.province'].search([('pid', '=', data.pid)])
                        if not province_id:
                            continue
                        lst_district_need_create.append(District.parser_class(data, pid=province_id.id))
                if lst_district_need_create:
                    self.create(lst_district_need_create)
            return Action.display_notification(_('Sync district successfully!'), _(Message.MSG_ACTION_SUCCESS))
        except Exception as e:
            raise UserError(_(f'Sync districts failed. Error: {str(e)}'))


class GHNWard(models.Model):
    _name = 'giaohangnhanh.ward'
    _order = 'did asc'
    _inherit = ['mail.thread']
    _description = 'Giao Hang Nhanh Wards'

    name = fields.Char(string='Ward Name', required=True, tracking=True)
    code = fields.Char(string='Code', required=True, tracking=True)
    did = fields.Many2one('giaohangnhanh.district', string='District', required=True, tracking=True)
    active = fields.Boolean(string='Active')

    @api.model
    def sync_wards(self):
        try:
            client = self.env['api.connect.instances'].generate_ghn_client_api()
            dataset = client.sync_wards()
            if dataset:
                lst_ward_need_create: list = []
                dataclass_ward: List[Ward] = [Ward(*Ward.parser_dict(rec)) for rec in dataset]
                lst_codes: List[str] = [rec.code for rec in dataclass_ward]
                lst_exists_ward: List[GHNWard] = self.search([('code', 'in', lst_codes)])
                lst_exists_ward_codes: List[str] = [rec.code for rec in lst_exists_ward]
                for data in dataclass_ward:
                    if data.code not in lst_exists_ward_codes:
                        district_id = self.env['giaohangnhanh.district'].search([('did', '=', data.did)])
                        if not district_id:
                            continue
                        lst_ward_need_create.append(Ward.parser_class(data, did=district_id.id))
                if lst_ward_need_create:
                    self.create(lst_ward_need_create)
            return Action.display_notification(_('Sync wards successfully!'), _(Message.MSG_ACTION_SUCCESS))
        except Exception as e:
            raise UserError(_(f'Sync wards failed. Error: {str(e)}'))

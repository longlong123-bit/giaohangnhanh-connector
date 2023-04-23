from typing import List
from odoo import fields, api, models, _
from odoo.exceptions import UserError
from odoo.addons.giaohangnhanh_connector.dataclass.giaohangnhanh_office import Office
from odoo.addons.api_connect_instances.common.action import Action
from odoo.addons.giaohangnhanh_connector.constants.ghn_constants import Const, Message


class GHNOffice(models.Model):
    _name = 'giaohangnhanh.office'
    _description = 'List Giao Hang Nhanh Post Office'

    name = fields.Char(string='Office name', requered=True, tracking=True)
    code = fields.Char(string='Code', requered=True, tracking=True)
    office_id = fields.Integer(string='Location ID', requered=True, tracking=True)
    email = fields.Char(string='Email', tracking=True)
    province_name = fields.Char(string='Province name', requered=True, tracking=True)
    district_name = fields.Char(string='District name', requered=True, tracking=True)
    ward_name = fields.Char(string='Ward name', requered=True, tracking=True)
    address = fields.Char(string='Address', requered=True, tracking=True)
    latitude = fields.Char(string='Latitude', requered=True, tracking=True)
    longitude = fields.Char(string='Longitude', requered=True, tracking=True)
    iframe_map = fields.Char(string='Iframe map')

    @api.model
    def sync_offices(self):
        try:
            client = self.env['api.connect.instances'].generate_ghn_client_api()
            dataset = client.sync_offices()
            if dataset:
                lst_office_need_create: list = []
                dataclass_office: List[Office] = [Office(*Office.parser_dict(rec)) for rec in dataset]
                lst_office_ids: List[int] = [rec.location_id for rec in dataclass_office]
                lst_exists_office: List[GHNOffice] = self.search([('office_id', 'in', lst_office_ids)])
                lst_exists_office_ids: List[int] = [rec.office_id for rec in lst_exists_office]
                for data in dataclass_office:
                    if data.location_id not in lst_exists_office_ids:
                        lst_office_need_create.append(Office.parser_class(data))
                if lst_office_need_create:
                    self.create(lst_office_need_create)
            return Action.display_notification(_('Sync office successfully!'), _(Message.MSG_ACTION_SUCCESS))
        except Exception as e:
            raise UserError(_(f'Sync office failed. Error: {str(e)}'))

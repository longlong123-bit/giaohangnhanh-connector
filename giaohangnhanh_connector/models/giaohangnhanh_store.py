from typing import List
from odoo import fields, api, models, _
from odoo.exceptions import UserError
from odoo.addons.giaohangnhanh_connector.dataclass.giaohangnhanh_store import Store
from odoo.addons.api_connect_instances.common.action import Action
from odoo.addons.giaohangnhanh_connector.constants.ghn_constants import Const, Message


class GHNStore(models.Model):
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
    active = fields.Boolean(string='Active')

    @api.model
    def sync_stores(self):
        try:
            client = self.env['api.connect.instances'].generate_ghn_client_api()
            dataset = client.sync_stores()
            if dataset.get('shops'):
                lst_store_need_create: list = []
                dataclass_store: List[Store] = [Store(*Store.parser_dict(rec)) for rec in dataset.get('shops')]
                lst_store_ids: List[int] = [rec.id for rec in dataclass_store]
                lst_exists_store: List[GHNStore] = self.search([('cid', 'in', lst_store_ids)])
                lst_exists_store_ids: List[int] = [rec.cid for rec in lst_exists_store]
                for data in dataclass_store:
                    if data.id not in lst_exists_store_ids:
                        did = self.env['giaohangnhanh.district'].search([('did', '=', data.district_id)])
                        wid = self.env['giaohangnhanh.ward'].search([('code', '=', data.ward_code)])
                        if not did or not wid:
                            continue
                        lst_store_need_create.append(Store.parser_class(data, pid=did.pid.id, did=did.id, wid=wid.id))
                if lst_store_need_create:
                    self.create(lst_store_need_create)
            return Action.display_notification(_('Sync stores successfully!'), _(Message.MSG_ACTION_SUCCESS))
        except Exception as e:
            raise UserError(_(f'Sync Store failed. Error: {str(e)}'))

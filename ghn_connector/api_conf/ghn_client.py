import logging
from odoo.tools.translate import _
from odoo.exceptions import UserError
from .ghn_connection import GHNConnection
from odoo.addons.ghn_connector.contanst.ghn_contanst import FuncName
from odoo.addons.ghn_connector.contanst.ghn_contanst import Method
_logger = logging.getLogger(__name__)


class GHNClient:
    def __init__(self, host, token, external_model):
        self.conn = GHNConnection(host, token, external_model)

    def sync_provinces(self):
        res = self.conn.execute_restful(FuncName.SyncProvinces, Method.GET)
        res = self.check_response(res)
        return res

    def sync_districts(self):
        res = self.conn.execute_restful(FuncName.SyncDistricts, Method.GET)
        res = self.check_response(res)
        return res

    def sync_wards(self):
        res = self.conn.execute_restful(FuncName.SyncWards, Method.GET)
        res = self.check_response(res)
        return res

    def sync_stores(self):
        res = self.conn.execute_restful(FuncName.SyncStores, Method.GET)
        res = self.check_response(res)
        return res

    def generate_store(self, payload):
        res = self.conn.execute_restful(FuncName.GenerateStore, Method.POST, **payload)
        res = self.check_response(res)
        return res

    def check_response(self, res):
        if res['code'] == 200:
            res = res['data']
        else:
            self.error(res)
        return res

    def error(self, data):
        _logger.error(f'{data}')
        msg = data.get('message', _('No description error'))
        raise UserError(_(f'Error: {msg}'))

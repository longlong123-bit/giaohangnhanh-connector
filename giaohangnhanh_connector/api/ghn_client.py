import logging
from odoo.tools.translate import _
from odoo.exceptions import UserError
from .ghn_connection import GHNConnection
from odoo.addons.giaohangnhanh_connector.constants.ghn_constants import FuncName
from odoo.addons.giaohangnhanh_connector.constants.ghn_constants import Method
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

    def get_list_pick_shift(self):
        res = self.conn.execute_restful(FuncName.GetPickShift, Method.GET)
        res = self.check_response(res)
        return res

    def get_list_service(self, payload):
        res = self.conn.execute_restful(FuncName.GetServices, Method.POST, **payload)
        res = self.check_response(res)
        return res

    def calculate_fee(self, payload):
        res = self.conn.execute_restful(FuncName.CalculateFee, Method.POST, **payload)
        res = self.check_response(res)
        return res

    def sync_offices(self):
        res = self.conn.execute_restful(FuncName.SyncPostOffices, Method.GET)
        res = self.check_response(res)
        return res

    def create_waybill(self, payload):
        res = self.conn.execute_restful(FuncName.CreateOrder, Method.POST, **payload)
        res = self.check_response(res)
        return res

    def cancel_order(self, payload):
        res = self.conn.execute_restful(FuncName.CancelOrder, Method.POST, **payload)
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

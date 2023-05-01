import requests
import json
import logging
from datetime import datetime
from odoo.exceptions import UserError
from odoo.tools.translate import _
from odoo.addons.giaohangnhanh_connector.constants.ghn_constants import Method
_logger = logging.getLogger(__name__)


class GHNConnection:

    def __init__(self, host, token, external_model):
        self.host = host
        self.token = token
        self.external_model = external_model

    def execute_restful(self, func_name, method, *args, **kwargs):
        try:
            endpoint_id = self.external_model.env['api.endpoint.config'].search([('name', '=', func_name)])
            if not endpoint_id:
                raise UserError(_(f'Function name {func_name} is not existed'))
            endpoint = endpoint_id.endpoint
            url = self.host + endpoint
            headers = {
                'Content-Type': 'application/json',
                'Token': self.token
            }
            if method == Method.GET:
                res = requests.get(url, params=kwargs, headers=headers, timeout=300)
            elif method == Method.POST:
                res = requests.post(url, json=kwargs, headers=headers, timeout=300)
            data = res.json()
            self.create_connect_history(func_name, method, url, json.dumps(kwargs), json.dumps(data.get('message', False)),
                                        data.get('code', False))
            if res.status_code != 200:
                raise UserError(_(f'Request failed with status: {res.status_code} - Message: {data["message"]}'))
            return data
        except Exception as e:
            raise e

    def _get_sequence_request_id(self):
        sequence = self.external_model.env['ir.sequence'].search([
            ('code', '=', 'api.connect.history'),
            ('prefix', '=', 'req-giaohangnhanh-'),
            ('active', '=', True)
        ])
        next_document = sequence.get_next_char(sequence.number_next_actual)
        self.external_model.env.cr.execute('''SELECT request_id FROM api_connect_history''')
        query_res = self.external_model.env.cr.fetchall()
        while next_document in [res[0] for res in query_res]:
            next_tmp = self.external_model.env['ir.sequence'].next_by_code('api.connect.history')
            next_document = next_tmp
        return next_document

    def create_connect_history(self, *args):
        create_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        uid = self.external_model.env.uid
        sequence = self._get_sequence_request_id()
        query = f"""
                    INSERT INTO api_connect_history (name, method, url, body, message, status, request_id, create_date, create_uid) 
                    VALUES ('{args[0]}', '{args[1]}', '{args[2]}', '{args[3]}', '{args[4]}', '{args[5]}', '{sequence}', '{create_date}', '{uid}')
                """
        query = query.replace('\n', '')
        self.external_model.env.cr.execute(query)
        self.external_model.env.cr.commit()
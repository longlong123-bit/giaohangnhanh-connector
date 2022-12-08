from odoo import fields, models, _
from odoo.exceptions import UserError
from odoo.tools.misc import ustr
import logging
import requests
_logger = logging.getLogger(__name__)
from odoo.addons.viettelpost_connector.clients.viettelpost_clients import ViettelPostClient
from odoo.addons.viettelpost_connector.contanst.viettelpost_contanst import Const
from odoo.addons.viettelpost_connector.contanst.viettelpost_contanst import Message


class ApiConnectConfig(models.Model):
    _name = 'api.connect.config'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'The config server information for API Giao Hang Nhanh'

    name = fields.Char(string='Name', required=True, tracking=True)
    code = fields.Char(string='Code', required=True, tracking=True)
    host = fields.Char(string='Host', required=True, tracking=True)
    token = fields.Text(string='Token', tracking=True, readonly=True)
    active = fields.Boolean(string='Active', default=True, tracking=True)
    endpoint_ids = fields.One2many('api.endpoint.config', 'api_connect_config_id', string='Endpoint')

    def btn_test_connection(self):
        self.ensure_one()
        try:
            request = requests.get(self.host, timeout=3)
            _logger.info(f'{request}')
        except UserError as e:
            raise e
        except Exception as e:
            raise UserError(_(f'Connection Test Failed! Here is what we got instead:\n {ustr(e)}'))
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Connection test successfully!"),
                "type": "success",
                "message": _("Everything seems properly set up!"),
                "sticky": False,
            },
        }


class ApiConnectHistory(models.Model):
    _name = 'api.connect.history'
    _description = 'Logging request api to Giao Hang Nhanh'
    _order = 'create_date desc'

    name = fields.Char(string='Request')
    status = fields.Integer(string='Status')
    message = fields.Char(string='Message')
    url = fields.Char(string='Url')
    method = fields.Char(string='Method')
    body = fields.Text(string='Body')


class ApiEndpointConfig(models.Model):
    _name = 'api.endpoint.config'
    _description = 'Configuration dynamic endpoint for host when there is a change of routes from Giao Hang Nhanh. '

    endpoint = fields.Char(string='Endpoint', required=True)
    name = fields.Char(string='Function name', required=True, readonly=True)
    api_connect_config_id = fields.Many2one('api.connect.config', string='Api connect config id')
    host = fields.Char(related='api_connect_config_id.host', string='Host')
    description = fields.Text(string='Description')
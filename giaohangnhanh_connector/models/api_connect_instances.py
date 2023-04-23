from typing import Dict, Optional, NoReturn
from odoo import models, _
from odoo.exceptions import UserError

from odoo.addons.giaohangnhanh_connector.api.ghn_client import GHNClient
from odoo.addons.giaohangnhanh_connector.constants.ghn_constants import Const, Message


class APIConnectInstances(models.Model):
    _inherit = 'api.connect.instances'
    _description = 'The config server information for API Instance Giao Hang Nhanh'

    def generate_ghn_client_api(self) -> GHNClient:
        instance_id = self.search([('code', '=', Const.INSTANCE_CODE), ('active', '=', True)])
        if not instance_id:
            raise UserError(_(Message.BASE_MSG))
        client = GHNClient(instance_id.host, instance_id.token, self)
        return client

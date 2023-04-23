from odoo import fields, models, _, api
from odoo.exceptions import UserError
from odoo.addons.giaohangnhanh_connector.constants.ghn_constants import Message


class CreateStoreWizard(models.Model):
    _name = 'create.store.wizard'
    _description = 'Form Odoo Create Store To Giao Hang Nhanh Dashboard'

    name = fields.Char(string='Name', required=True)
    phone = fields.Char(string='Phone', required=True)
    address = fields.Char(string='Address', required=True)
    wid = fields.Many2one('giaohangnhanh.ward', string='Ward', required=True)
    did = fields.Many2one('giaohangnhanh.district', string='District', required=True)

    @api.model
    def create_store(self):
        action = self.env.ref('giaohangnhanh_connector.create_store_wizard_action').read()[0]
        return action

    def ghn_create_store(self):
        client = self.env['api.connect.instances'].generate_client_api_ghn()
        try:
            payload = {
                'name': self.name,
                'phone': self.phone,
                'address': self.address,
                'ward_code': self.wid.code,
                'district_id': self.did.did
            }
            client.generate_store(payload)
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": _("Create store successfully!"),
                    "type": "success",
                    "message": _(Message.MSG_ACTION_SUCCESS),
                    "sticky": False,
                    "next": {"type": "ir.actions.client", "tag": "reload"},
                },
            }
        except Exception as e:
            raise UserError(_(f'Create store failed. Error: {e}'))

    @api.onchange('did')
    def _onchange_did(self):
        for rec in self:
            if rec.did:
                return {
                    'domain':
                        {
                            'wid': [('did', '=', rec.did.id)]
                        },
                }


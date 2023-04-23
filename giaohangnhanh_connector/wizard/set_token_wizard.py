from odoo import models, _, api, fields


class SetTokenWizard(models.TransientModel):
    _name = 'set.token.wizard'
    _description = 'This module is used as a set token for the Giao Hang Nhanh instance'

    instance_id = fields.Many2one('api.connect.instances', string='Instance', readonly=True)
    token = fields.Char(string='Token')

    @api.model
    def default_get(self, fields_list):
        values = super(SetTokenWizard, self).default_get(fields_list)
        if not values.get('instance_id') and 'active_model' in self._context \
                and self._context['active_model'] == 'api.connect.instances':
            values['instance_id'] = self._context.get('active_id')
        return values

    def action_set_token(self):
        self.instance_id.write({'token': self.token})
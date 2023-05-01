from odoo import fields, models, api


class GHNService(models.Model):
    _name = 'giaohangnhanh.service'
    _description = 'List of supported services of Giao Hang Nhanh'

    name = fields.Char(string='Name', required=True)
    service_type_id = fields.Integer(string='Service Type Id')
    service_id = fields.Integer(string='Service Id')

    @api.depends('name', 'service_id')
    def name_get(self):
        res = []
        for record in self:
            name = record.name
            if record.service_id:
                name = f'[{record.service_id}] - {name}'
            res.append((record.id, name))
        return res

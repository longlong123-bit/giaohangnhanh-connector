from odoo import fields, models, api


class GHNProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = 'Customize Attributes'

    gross_length = fields.Float(string='Length (cm)', required=True)
    gross_width = fields.Float(string='Width (cm)', required=True)
    gross_height = fields.Float(string='Height (cm)', required=True)

    cm_uom_name = fields.Char(string='Height unit of measure label', compute='_compute_cm_uom_name')

    @api.model
    def _get_cm_uom_name_from_ir_config_parameter(self):
        return self._get_common_uom_id_from_ir_config_parameter().display_name

    def _compute_cm_uom_name(self):
        self.cm_uom_name = self._get_cm_uom_name_from_ir_config_parameter()

    @api.model
    def _get_common_uom_id_from_ir_config_parameter(self):
        """ Get the unit of measure to interpret the `height, width, depth` field. By default, we considerer
        that height, width, depth are expressed in cm. Users can configure to express them in millimeter
        by adding an ir.config_parameter record with "product.product_in_mm" as key
        and "1" as value.
        -- It is recommended to use cm in units of Giao Hang Nhanh Carrier --
        """
        product_cm_in_lbs_param = self.env['ir.config_parameter'].sudo().get_param('product.product_in_mm')
        if product_cm_in_lbs_param == '1':
            return self.env.ref('uom.product_uom_millimeter')
        else:
            return self.env.ref('uom.product_uom_cm')
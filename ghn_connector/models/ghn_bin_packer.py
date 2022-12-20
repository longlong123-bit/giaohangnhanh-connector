from odoo import fields, models, api


class GHNPinPacker(models.Model):
    _name = 'ghn.bin.packer'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Bin Packer Giao Hang Nhanh Management'

    name = fields.Char(string='Name', required=True, tracking=True)
    width = fields.Float(string='Width', required=True, tracking=True)
    height = fields.Float(string='Height', required=True, tracking=True)
    depth = fields.Float(string='Depth', required=True, tracking=True)
    vol_weight = fields.Float(string='Weight', compute='_compute_vol_weight', tracking=True, store=True)
    volume = fields.Float(string='Volume', compute='_compute_volume', tracking=True, store=True)
    quantity = fields.Float(string='Quantity', tracking=True)

    cm_uom_name = fields.Char(string='Height unit of measure label', compute='_compute_cm_uom_name')
    weight_uom_name = fields.Char(string='Weight unit of measure label', compute='_compute_weight_uom_name')
    volume_uom_name = fields.Char(string='Volume unit of measure label', compute='_compute_volume_uom_name')
    unit_uom_name = fields.Char(string='Unit of measure label', compute='_compute_unit_uom_name')

    @api.depends('height', 'width', 'depth')
    def _compute_vol_weight(self):
        for rec in self:
            rec.vol_weight = rec.width * rec.height * rec.depth / 5000 * 1000

    @api.depends('height', 'width', 'depth')
    def _compute_volume(self):
        for rec in self:
            rec.volume = rec.width * rec.height * rec.depth

    @api.model
    def _get_unit_uom_name_from_ir_config_parameter(self):
        return self._get_unit_uom_id_from_ir_config_parameter().display_name

    def _compute_unit_uom_name(self):
        self.unit_uom_name = self._get_unit_uom_name_from_ir_config_parameter()

    @api.model
    def _get_unit_uom_id_from_ir_config_parameter(self):
        return self.env.ref('uom.product_uom_unit')

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

    @api.model
    def _get_weight_uom_name_from_ir_config_parameter(self):
        return self._get_weight_uom_id_from_ir_config_parameter().display_name

    def _compute_weight_uom_name(self):
        self.weight_uom_name = self._get_weight_uom_name_from_ir_config_parameter()

    @api.model
    def _get_weight_uom_id_from_ir_config_parameter(self):
        """ Get the unit of measure to interpret the `weight` field. By default, we considerer
        that weights are expressed in kilograms. Users can configure to express them in kilogram
        by adding an ir.config_parameter record with "product.weight_in_gram" as key
        and "0" as value.
        """
        product_weight_in_lbs_param = self.env['ir.config_parameter'].sudo().get_param('product.weight_in_gram')
        if product_weight_in_lbs_param == '1':
            return self.env.ref('uom.product_uom_gram')
        else:
            return self.env.ref('uom.product_uom_kgm')

    @api.model
    def _get_volume_uom_name_from_ir_config_parameter(self):
        return self._get_volume_uom_id_from_ir_config_parameter().display_name

    def _compute_volume_uom_name(self):
        self.volume_uom_name = self._get_volume_uom_name_from_ir_config_parameter()

    @api.model
    def _get_volume_uom_id_from_ir_config_parameter(self):
        """ Get the unit of measure to interpret the `volume` field. By default, we consider
        that volumes are expressed in cubic meters. Users can configure to express them in cubic feet
        by adding an ir.config_parameter record with "product.volume_in_cubic_feet" as key
        and "1" as value.
        """
        product_length_in_feet_param = self.env['ir.config_parameter'].sudo().get_param('product.volume_in_cubic_feet')
        if product_length_in_feet_param == '1':
            return self.env.ref('uom.product_uom_cubic_foot')
        else:
            return self.env.ref('uom.product_uom_cubic_meter')

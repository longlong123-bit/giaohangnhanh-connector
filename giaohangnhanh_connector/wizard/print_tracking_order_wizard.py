import requests
import base64
import re
import io
from lxml import html
from odoo import models, _, api, fields
from odoo.exceptions import UserError
from odoo.tools import ustr
from odoo.addons.giaohangnhanh_connector.constants.ghn_constants import Const, Message


class PrintTrackingOrderWizard(models.TransientModel):
    _name = 'print.tracking.order.wizard'
    _description = 'This module is used as print Carrier Tracking Ref Information of the Giao Hang Nhanh'

    shipment_id = fields.Many2one('giaohangnhanh.shipment', string='Shipment', readonly=True)

    @api.model
    def default_get(self, fields_list):
        values = super(PrintTrackingOrderWizard, self).default_get(fields_list)
        if not values.get('shipment_id') and 'active_model' in self._context \
                and self._context['active_model'] == 'giaohangnhanh.shipment':
            values['shipment_id'] = self._context.get('active_id')
        return values

    def _get_payload_print_order(self) -> dict:
        payload = {
            'order_codes': [self.shipment_id.carrier_tracking_ref]
        }
        return payload

    def _get_template_waybill(self, mode='pdf'):
        report = self.env.ref('giaohangnhanh_connector.action_print_waybill')
        if mode == 'pdf':
            content, __ = report.render_qweb_pdf(self.ids)
        else:
            content, __ = report.render_qweb_html(self.ids)
        return content, report

    @staticmethod
    def _replace_handle_cont(cont: str) -> str:
        regex = re.compile(r"id=\"(process-bar|myBar|value-percent)\"|( page-break|background|Đang tải 0%)")
        cont = re.sub(regex, '', cont)
        return cont

    def action_print_tracking_order(self):
        try:
            client = self.env['api.connect.instances'].generate_ghn_client_api()
            payload = self._get_payload_print_order()
            result = client.print_order(payload)
            if result.get('token'):
                token = result.get('token')
                instance_id = self.env['api.connect.instances'].sudo().search([('code', '=', 'giaohangnhanh')])
                type_print = self._context.get('type_print')
                if type_print == 'a5':
                    link = Const.URL_PRINT_A5.format(host=instance_id.host, token=token)
                elif type_print == '80x80':
                    link = Const.URL_PRINT_80x80.format(host=instance_id.host, token=token)
                elif type_print == '52x70':
                    link = Const.URL_PRINT_80x80.format(host=instance_id.host, token=token)
                else:
                    raise UserError(_('The type print not found.'))
                response = requests.get(link)
                template, report = self._get_template_waybill()
                response.raise_for_status()
                cont = response.content.decode().strip()
                cont = self._replace_handle_cont(cont)
                cont = ('<base href="%s" target="_blank">' % response.url.rsplit('/', 1)[0]) + cont
                content = report._run_wkhtmltopdf([cont.encode()])
                content = report._merge_pdfs([io.BytesIO(template), io.BytesIO(content)])
                shipment_attach = {
                    'name': f'{self.shipment_id.delivery_order_id.sale_id.name}.pdf',
                    'res_model': self.shipment_id._name,
                    'res_id': self.shipment_id.id,
                    'datas': base64.b64encode(content),
                    'public': True
                }
                # delivery_attach = {
                #     'name': f'{self.shipment_id.delivery_order_id.sale_id.name}.html',
                #     'res_model': self.shipment_id.delivery_order_id._name,
                #     'res_id': self.shipment_id.delivery_order_id.id,
                #     'datas': base64.b64encode(cont.encode()),
                #     'public': True
                # }
                # sale_order_attach = {
                #     'name': f'{self.shipment_id.delivery_order_id.sale_id.name}.html',
                #     'res_model': self.shipment_id.delivery_order_id.sale_id._name,
                #     'res_id': self.shipment_id.delivery_order_id.sale_id.id,
                #     'datas': base64.b64encode(cont.encode()),
                #     'public': True
                # }
                attach_id = self.env['ir.attachment'].sudo().create([shipment_attach])

        except Exception as e:
            raise UserError(ustr(e))

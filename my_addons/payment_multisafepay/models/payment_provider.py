import logging

import requests
from werkzeug import urls

from odoo import models, fields
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('msp', "Multisafepay")],
        ondelete={'msp': 'set default'})
    msp_api_key_test = fields.Char(
        string="MSP merchant key",
        help="The code of the merchant account to use with this provider.",
        required_if_provider='msp'
    )

    def _msp_make_request(self, endpoint, data=None, method='POST'):
        """ Make a request at msp endpoint."""
        self.ensure_one()
        endpoint = f'/v1/{endpoint.strip("/")}'
        url = urls.url_join('https://testapi.multisafepay.com/', endpoint)
        headers = {
            'api_key': self.msp_api_key_test,
            "content-type": "application/json",
            "accept": "application/json"
        }

        try:
            response = requests.request(method, url, json=data, headers=headers,
                                        timeout=60)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            _logger.exception("unable to communicate with MSP: %s", url)
            raise ValidationError(
                "C: " + "Could not establish the connection to the API.")
        return response.json()

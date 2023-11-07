import logging
import pprint

from werkzeug import urls

from odoo.addons.payment_multisafepay.controllers.main import MSPController
from odoo import models

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        """ Override of payment to return MSP-specific rendering values."""
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'msp':
            return res

        payload = self._msp_prepare_payment_request_payload()
        _logger.info("sending '/json' request for link creation:\n%s",
                     pprint.pformat(payload))
        payment_data = self.provider_id._msp_make_request('/json/orders',
                                                          data=payload)
        checkout_url = payment_data['data']['payment_url']
        parsed_url = urls.url_parse(checkout_url)
        url_params = urls.url_decode(parsed_url.query)
        return {'url': checkout_url, 'url_params': url_params}

    def _msp_prepare_payment_request_payload(self):
        """ Create the payload for the payment request based on the transaction values."""
        base_url = self.provider_id.get_base_url()
        redirect_url = urls.url_join(base_url, MSPController._return_url)
        return {
            "type": "redirect",
            "order_id": self.id,
            "currency": self.currency_id.name,
            "amount": self.amount * 100,
            "description": self.reference,
            "payment_options": {
                "redirect_url": f'{redirect_url}?ref={self.reference}',
                "cancel_url": base_url + 'shop/payment',
            },
            "locale": self.partner_lang,
        }

    def _process_notification_data(self, notification_data):
        """ Override of `payment` to process the transaction based on msp
        data."""
        super()._process_notification_data(notification_data)
        if self.provider_code != 'msp':
            return
        self._set_done()


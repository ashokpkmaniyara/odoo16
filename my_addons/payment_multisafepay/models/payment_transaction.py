import logging
import pprint

# from setuptools._entry_points import _
from werkzeug import urls

from odoo.addons.payment_multisafepay.controllers.main import MSPController
from odoo import models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'msp':
            return res

        payload = self._msp_prepare_payment_request_payload()
        print('payload=', payload)
        _logger.info("sending '/json' request for link creation:\n%s",
                     pprint.pformat(payload))
        payment_data = self.provider_id._msp_make_request('/json/orders',
                                                          data=payload)
        print('payment_data=', payment_data)

        # self.provider_reference = payment_data.get('id')

        checkout_url = payment_data['data']['payment_url']
        parsed_url = urls.url_parse(checkout_url)
        url_params = urls.url_decode(parsed_url.query)
        return {'url': checkout_url, 'url_params': url_params}

    def _msp_prepare_payment_request_payload(self):
        base_url = self.provider_id.get_base_url()
        redirect_url = urls.url_join(base_url, MSPController._return_url)
        print(self.read())

        return {
            "type": "redirect",
            "order_id": self.id,
            "gateway": self.provider_code,
            "currency": self.currency_id.name,
            "amount": self.amount,
            "description": self.reference,
            "payment_options": {
                "notification_url": "",
                "notification_method": "POST",
                "redirect_url": f'{redirect_url}?ref={self.reference}',
                "cancel_url": base_url+'shop/payment',
                "close_window": True
            },
            "customer": {
                'partner_id': self.partner_id.id,
                "locale": self.partner_lang,
                # "first_name": self.partner_name,
                # "last_name": self.partner_name,
                # "company_name": self.company_id.name,
                # "address1": self.partner_address,
                # "house_number": self.partner_address,
                # "zip_code": self.partner_zip,
                # "city": self.partner_city,
                # "country": self.partner_country_id.name,
                # "phone": self.partner_phone,
                # "email": self.partner_email,
                # "referrer": "https://testapi.multisafepay.com",
                # "user_agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
            },
        }
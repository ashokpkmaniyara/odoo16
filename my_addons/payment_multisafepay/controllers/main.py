import logging
import pprint

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class MSPController(http.Controller):
    _return_url = '/payment/msp/return'

    @http.route(
        _return_url, type='http', auth='public', methods=['GET', 'POST'],
        csrf=False,
        save_session=False
    )
    def msp_return_from_checkout(self, **data):
        _logger.info("handling redirection from MSP with data:\n%s",
                     pprint.pformat(data))
        request.env[
            'payment.transaction'].sudo().search(
            [('reference', '=', data.get('ref'))])._handle_notification_data(
            'msp', data)

        return request.redirect('/payment/status')

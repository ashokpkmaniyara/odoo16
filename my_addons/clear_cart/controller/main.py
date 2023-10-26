# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import Controller, route, request


class WebsiteSale(Controller):

    @http.route(['/clear/cart'], type='http', auth="public", website=True)
    def clear_cart(self):
        order = request.website.sale_get_order()
        order.unlink()
        return request.redirect('/shop/cart')


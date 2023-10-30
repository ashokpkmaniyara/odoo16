# -*- coding: utf-8 -*-
from odoo.addons.portal.controllers import portal
from odoo.http import Controller, route, request


class ManufacturingOrder(Controller):

    @route('/my/mo', auth='user', website=True)
    def fetch_mo(self):
        mo = request.env['mrp.production'].sudo().search(
            [('customer_id', '=', request.env.user.partner_id.id)])
        return request.render('mo_in_website.my_manufacturing_order_portal',
                              {'orders': mo})


class ManufacturingCount(portal.CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'mo_count' in counters:
            values['mo_count'] = request.env[
                'mrp.production'].sudo().search_count(
                [('customer_id', '=', request.env.user.partner_id.id)])
        return values

# -*- coding: utf-8 -*-
from odoo import models, fields


class ProductOwner(models.Model):
    _inherit = 'product.product'

    owner_id = fields.Many2one('res.partner', 'Owner',
                               help='set owner for the product')


class LoadProductField(models.Model):
    _inherit = 'pos.session'

    def _loader_params_product_product(self):
        result = super()._loader_params_product_product()
        result['search_params']['fields'].extend(['owner_id'])
        return result

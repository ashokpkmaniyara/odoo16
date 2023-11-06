# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PurchaseLimit(models.Model):
    _inherit = 'res.partner'

    purchase_limit = fields.Boolean(string='Purchase Limit', help='specify a '
                                                                  'limit for '
                                                                  'pos '
                                                                  'purchase')
    limit = fields.Float(help='specify a max limit')

    @api.onchange('purchase_limit')
    def _onchange_discount_limit(self):
        """Set limit to 0 when purchase_limit is unticked."""
        if not self.purchase_limit:
            self.limit = 0

    @api.constrains('limit')
    def _check_limit(self):
        """function to check all the given value is positive"""
        if self.purchase_limit and self.limit < 0:
            raise ValidationError(
                "Purchase Limit must be a positive value.")


class LoadProductField(models.Model):
    _inherit = 'pos.session'

    def _loader_params_res_partner(self):
        result = super()._loader_params_res_partner()
        result['search_params']['fields'].extend(
            ['limit', 'purchase_limit'])
        return result



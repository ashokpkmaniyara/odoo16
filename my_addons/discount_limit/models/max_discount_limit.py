# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ConfSetting(models.TransientModel):
    """class created for inheriting settings and add a custom field discount limit"""
    _inherit = ["res.config.settings"]

    discount_limit = fields.Boolean(string="Discount Limit", store=True,
                                    config_parameter='discount_limit.discount_limit')
    max_limit = fields.Integer(config_parameter='discount_limit.max_limit', store=True)

    @api.onchange('discount_limit')
    def _onchange_discount_limit(self):
        """Set max_limit to 0 when discount_limit is unticked."""
        if not self.discount_limit:
            self.max_limit = 0

    @api.constrains('max_limit')
    def _check_max_limit(self):
        """function to check all the given value is positive"""
        if self.discount_limit and self.max_limit < 0:
            raise ValidationError("Max Discount Limit must be a positive value.")

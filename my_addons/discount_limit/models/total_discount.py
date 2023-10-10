# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    """class for inheriting sales order"""
    _inherit = "sale.order"

    current_month = fields.Char(string="Current Month", store=True)
    total_discount_month = fields.Float(string="Total Discount for the Month",
                                        compute="_compute_total_discount_month",
                                        store=True)
    warning = fields.Boolean(default=False)

    @api.depends("order_line.discount", "order_line.price_unit",
                 "current_month")
    def _compute_total_discount_month(self):
        """function to compute the total discount amount for the current month"""
        for order in self:
            order.current_month = fields.Date.context_today(self).strftime('%m')
            if order.current_month:
                orders_in_month = self.env['sale.order'].search([
                    ('current_month', '=', order.current_month),
                ])

                order.total_discount_month = sum(
                    (
                                line.discount / 100) * line.price_unit * line.product_uom_qty
                    for line in orders_in_month.mapped('order_line')
                )
            else:
                order.total_discount_month = 0.0

    @api.constrains('total_discount_month')
    def _check_discount_limit(self):
        """function to check the discount limit is exceeded, if exceeded to show a warning message"""
        for order in self:
            config_settings = self.env['res.config.settings'].search([],
                                                                     order='id desc',
                                                                     limit=1)
            max_limit = config_settings.max_limit

            if max_limit and max_limit < order.total_discount_month:
                self.warning = True

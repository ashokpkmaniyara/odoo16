# -*- coding: utf-8 -*-
from odoo import models, fields


class ThresholdQuantity(models.TransientModel):
    """class for inheriting settings and added some fields"""
    _inherit = 'res.config.settings'

    stock_warning = fields.Boolean(string='Stock Warning',
                                   help='enable to notify the stock manager if the stock is low',
                                   config_parameter='stock_warning_email.stock_warning')
    threshold_qty = fields.Integer(string='Threshold Quantity',
                                   help='set a minimum quntity required',
                                   config_parameter='stock_warning_email.threshold_qty')
    product_id = fields.Many2one('product.product', string='Product',
                                 help='select a product',
                                 config_parameter='stock_warning_email.product_id')
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse',
                                   help='select a warehouse',
                                   config_parameter='stock_warning_email.warehouse_id')

# -*- coding: utf-8 -*-
from odoo import fields, models


class ProductWise(models.Model):
    _name = 'product.wise'

    product_category_id = fields.Many2one('product.category',
                                       string='Product Category',
                                       help='select a category')
    product_id = fields.Many2one('product.product', string='Product',
                              help='select the product',domain="[('categ_id', '=', product_category_id)]")
    rate = fields.Float(string='Rate', help='specify the rate of the product')
    max_amount = fields.Float(string='Max Commission Amount',
                              help='specify the maximum commission amount')
    product_commission_id = fields.Many2one('crm.commission')
# -*- coding: utf-8 -*-

from odoo import models, fields


class PurchaseWizard(models.TransientModel):
    """created model of purchase.wizard to crate a wizard view"""
    _name = 'purchase.wizard'

    quantity = fields.Integer(string='Quantity', default=1,
                              help='specify the quantity')
    price = fields.Float(string='Price',
                         help='specify the price of the product')
    product_id = fields.Many2one('product.template', string="Product",
                                 readonly=1)
    vendor_id = fields.Many2one('res.partner', string='Vendor', readonly=1)

    def action_done(self):
        """function for submit button in wizard view to create po if not
        existing rfq with same vendor in purchase page and if exist use that
        rfq and add order line only"""
        product_product_id = self.product_id.product_variant_id.id
        existing_rfq = self.env['purchase.order'].search(
            [('partner_id', '=', self.vendor_id.id), ('state', '=', 'draft')],
            limit=1)
        if not existing_rfq:
            existing_rfq = self.env['purchase.order'].create({
                'partner_id': self.vendor_id.id,
                'order_line': [fields.Command.create({
                    'product_id': product_product_id,
                    'product_qty': self.quantity,
                    'price_unit': self.price,
                })]
            })
        else:
            existing_rfq.order_line = [fields.Command.create({
                'product_id': product_product_id,
                'product_qty': self.quantity,
                'price_unit': self.price,
            })]
        existing_rfq.button_confirm()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchase Oder',
            'res_model': 'purchase.order',
            'view_mode': 'form',
            'res_id': existing_rfq.id,
            'target': 'current',
        }

# -*- coding: utf-8 -*-
from odoo import models, fields, api


class MultipleSO(models.Model):
    """model for inheriting invoice form and adding a new field"""
    _inherit = ["account.move"]

    related_so_ids = fields.Many2many("sale.order", string='Related SO',
                                      domain="[('partner_id', '=', partner_id),('invoice_status','=','to invoice')]")

    @api.constrains("related_so_ids")
    def _change_related_so(self):
        """to make all the sale order lines in multiple sale orders into
        invoice line. If there is same product then to merge the product and
        create the invoice on save."""
        self.invoice_line_ids = [fields.Command.clear()]
        invoice_line = {}
        for sale_order in self.related_so_ids:
            sale_order.picking_ids.button_validate()
            for order_line in sale_order.order_line:
                if order_line.product_id.id in invoice_line:
                    invoice_line[order_line.product_id.id][
                        'quantity'] += order_line.product_uom_qty
                    invoice_line[order_line.product_id.id][
                        'sale_line_ids'].append(
                        fields.Command.link(order_line.id))
                else:
                    invoice_line[order_line.product_id.id] = {
                        'product_id': order_line.product_id.id,
                        'quantity': order_line.product_uom_qty,
                        'price_unit': order_line.price_unit,
                        'sale_line_ids': [fields.Command.link(order_line.id)]
                    }
        self.invoice_line_ids = [fields.Command.create(values) for values in
                                 invoice_line.values()]


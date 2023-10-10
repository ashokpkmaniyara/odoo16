# -*- coding: utf-8 -*-
from odoo import models
from odoo.exceptions import ValidationError


class AutomatedPurchase(models.Model):
    """class to inherit model product.template"""
    _inherit = ['product.template']

    def automated(self):
        """function for a button in product view to view the wizard view"""
        if self.seller_ids:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Wizard',
                'view_mode': 'form',
                'res_model': 'purchase.wizard',
                'view_id': self.env.ref('automated_purchase_order.purchase_wizard_view_form').id,
                'target': 'new',
                'context': {
                    'default_price': self.list_price,
                    'default_product_id': self.id,
                    'default_vendor_id': self.seller_ids[0].partner_id.id
                }
            }
        else:
            raise ValidationError('Need to set a vendor')

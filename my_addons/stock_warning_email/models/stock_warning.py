# -*- coding: utf-8 -*-
from odoo import models


class StockWarning(models.Model):
    _name = 'stock.warning'

    def stock_warning_email(self):
        """function for sending the email to the stock manager if stock is
        low"""
        warning = self.env['ir.config_parameter'].sudo().get_param(
            'stock_warning_email.stock_warning')
        manager = self.env.ref('stock.group_stock_manager').users
        product_config_qty = self.env['ir.config_parameter'].sudo().get_param(
            'stock_warning_email.product_id')
        threshold = self.env['ir.config_parameter'].sudo().get_param(
            'stock_warning_email.threshold_qty')
        warehouse = self.env['ir.config_parameter'].sudo().get_param(
            'stock_warning_email.warehouse_id')
        available_qty = self.env['product.product'].browse(
            int(product_config_qty)).qty_available
        if warning and threshold and warehouse and product_config_qty and int(
                available_qty) <= int(threshold):
            template = self.env.ref(
                'stock_warning_email.stock_warning_email_template')
            data = {
                'product_id': int(product_config_qty),
                'warehouse': self.env['stock.warehouse'].browse(
                    int(warehouse)).name,
                'product': self.env['product.product'].browse(
                    int(product_config_qty)).name,
                'available_qty': available_qty,
                'threshold_qty': threshold,
                'company_name': self.env.user.company_id.name
            }
            for user in manager:
                email_values = {'email_to': user.email,
                                'email_from': self.env.user.email,
                                'subject': 'REMINDER: STOCK IS LOW'}
                template = template.with_context(data)
                template.send_mail(user.id, email_values=email_values,
                                   force_send=True)

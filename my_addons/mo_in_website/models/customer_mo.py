# -*- coding: utf-8 -*-
from odoo import models, fields


class ManufacturingOrders(models.Model):
    _inherit = 'mrp.production'

    customer_id = fields.Many2one('res.partner', string='Customer',
                                  help='select a customer')

# -*- coding: utf-8 -*-
from odoo import models, fields


class InvoicePage(models.Model):
    """model for invoice page with modified fields"""
    _inherit = ['account.move']

    event_type = fields.Char(string='Event Type')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    duration = fields.Integer(string='Duration')
    guest = fields.Integer(string='Guest')


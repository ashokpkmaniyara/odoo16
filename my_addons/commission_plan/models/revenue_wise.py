# -*- coding: utf-8 -*-
from odoo import fields, models, api, exceptions


class RevenueWise(models.Model):
    """class for revenue wise with essential fields"""
    _name = 'revenue.wise'

    sequence = fields.Char(compute='_compute_sequence', string='Sequence', help='generate sequence automatically')
    from_amount = fields.Float(string='From Amount', help='starting of amount limit')
    to_amount = fields.Float(string='To Amount', help='ending of amount limit')
    rate = fields.Float(string='Rate', help='specify the rate')
    revenue_commission_id = fields.Many2one('crm.commission')


    @api.depends('revenue_commission_id')
    def _compute_sequence(self):
        """function to generate sequence number for natural number"""
        number = 1
        seq = self.mapped('revenue_commission_id')
        for rec in seq.revenue_wise_ids:
            rec.sequence = number
            number += 1

    @api.constrains("from_amount", "to_amount")
    def _check_amounts(self):
        """function to check the to_amount is greater than from_amount otherwise raise exception"""
        if self.to_amount < self.from_amount:
            raise exceptions.ValidationError(
                "The From Amount limit cannot be greater than To Amount.")

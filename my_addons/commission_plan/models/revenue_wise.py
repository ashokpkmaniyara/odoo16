# -*- coding: utf-8 -*-
from odoo import fields, models, api, exceptions


class RevenueWise(models.Model):
    _name = 'revenue.wise'

    sequence = fields.Char(compute='_compute_sequence')
    from_amount = fields.Float(string='From Amount')
    to_amount = fields.Float(string='To Amount')
    rate = fields.Float(string='Rate')
    revenue_commission_id = fields.Many2one('crm.commission')
    # graduated_commission_id = fields.Many2one('crm.commission')

    @api.depends('revenue_commission_id')
    def _compute_sequence(self):
        number = 1
        seq = self.mapped('revenue_commission_id')
        for rec in seq.revenue_wise_ids:
            rec.sequence = number
            number += 1

    # @api.depends('graduated_commission_id')
    # def _compute_sequence(self):
    #     number = 1
    #     seq = self.mapped('graduated_commission_id')
    #     for rec in seq.graduated_ids:
    #         rec.sequence = number
    #         number += 1

    @api.constrains("from_amount", "to_amount")
    def _check_amounts(self):
        if self.to_amount < self.from_amount:
            raise exceptions.ValidationError("The From Amount limit cannot be greater than To Amount.")

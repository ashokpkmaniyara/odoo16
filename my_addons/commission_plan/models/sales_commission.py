# -*- coding: utf-8 -*-
from odoo import models, fields


class SaleOrder(models.Model):
    """class for inheriting sale order"""
    _inherit = 'sale.order'

    commission_amount = fields.Float(string='Commission', readonly=1, help='show the commission amount')

    def action_confirm(self):
        """function for sale order confirm button"""
        res = super().action_confirm()

        commission_amount = 0
        commission_plan_type = (
            self.user_id.commission_plan_id.type if self.user_id.commission_plan_id
            else self.team_id.commission_plan_id.type)
        if commission_plan_type == 'revenue_wise':
            commission_plan_wise = (
                self.user_id.commission_plan_id.revenue_wise if self.user_id.commission_plan_id
                else self.team_id.commission_plan_id.revenue_wise)
            if commission_plan_wise in ('straight', 'graduated'):
                commission_plan = (
                    self.user_id.commission_plan_id if self.user_id.commission_plan_id
                    else self.team_id.commission_plan_id)
                for line in commission_plan.revenue_wise_ids:
                    if commission_plan_wise == 'straight':
                        if line.from_amount <= self.amount_total <= line.to_amount:
                            commission_amount = self.amount_total * (
                                    line.rate / 100)
                    elif commission_plan_wise == 'graduated':
                        if line.from_amount <= self.amount_total <= line.to_amount:
                            first = self.amount_total
                            for rec in commission_plan.revenue_wise_ids:
                                if rec.to_amount <= line.to_amount:
                                    new = (first - rec.to_amount)
                                    if new >=0:
                                        new = rec.to_amount
                                        commission_amount += new * (rec.rate/100)
                                        first = first-new
                                        if first == 0:
                                            break
                                        print(commission_amount)
                                    else:
                                        commission_amount += abs(new) * (rec.rate/100)
                                        print(commission_amount)

            self.commission_amount = commission_amount
        else:
            commission_plan = (
                self.user_id.commission_plan_id if self.user_id.commission_plan_id
                else self.team_id.commission_plan_id)
            for order_line in self.order_line:
                for line in commission_plan.product_wise_ids:
                    if line.product_id:
                        if line.product_id == order_line.product_template_id:
                            max_cost = order_line.price_subtotal * (
                                    line.rate / 100)
                            if max_cost > line.max_amount:
                                max_cost = line.max_amount
                            commission_amount += max_cost
                    else:
                        if line.product_category_id == order_line.product_template_id.categ_id:
                            max_cost = order_line.price_subtotal * (
                                    line.rate / 100)
                            if max_cost > line.max_amount:
                                max_cost = line.max_amount
                            commission_amount += max_cost

            self.commission_amount = commission_amount

        return res

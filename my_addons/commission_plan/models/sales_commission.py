# -*- coding: utf-8 -*-
from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    commission_amount = fields.Float(string='Commission', readonly=1)
    def action_confirm(self):
        res = super().action_confirm()
        # print(self.user_id.commission_plan_id.revenue_wise)
        if self.user_id.commission_plan_id.type.revenue_wise == 'straight' or self.team_id.commission_plan_id.type.revenue_wise == 'straight':
            if self.user_id.commission_plan_id:
                self.commission_amount = self.amount_total/self.user_id.commission_plan_id.revenue_wise_ids.rate
            elif self.team_id.commission_plan_id:
                self.commission_amount = self.amount_total / self.team_id.commission_plan_id.revenue_wise_ids.rate
            print(self.commission_amount)
        else:
            for line in self.order_line:
                
        return res

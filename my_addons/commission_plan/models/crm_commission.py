# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import UserError


class CommissionPlan(models.Model):
    """to create new model crm.commission"""
    _name = 'crm.commission'
    _description = 'Commission Plan'
    _rec_name = "name"

    name = fields.Char(string='Name', help='name of the commission plan',
                       required=1)
    active = fields.Boolean(string='Active', help='enable to activate the plan',
                            default=1)
    start_date = fields.Date(string='Start Date', help='specify the start date',
                             required=1)
    end_date = fields.Date(string='End Date', help='specify the end date',
                           required=1)
    type = fields.Selection(
        [('product_wise', 'Product wise'), ('revenue_wise', 'Revenue Wise')],
        help='select the commission type', default='product_wise', required=1)
    product_wise_ids = fields.One2many('product.wise',
                                       inverse_name='product_commission_id')
    revenue_wise_ids = fields.One2many('revenue.wise',
                                       inverse_name='revenue_commission_id')
    revenue_wise = fields.Selection(
        [('straight', 'Straight'), ('graduated', 'Graduated')],
        help='select the revenue type', required=1, default='straight')

    @api.onchange('type')
    def _onchange_type(self):
        """for changing the selection the data also delete for the previous selection for field type"""
        if self.type != 'revenue_wise':
            self.revenue_wise_ids.unlink()
            self.type = 'product_wise'
        else:
            self.product_wise_ids.unlink()
            self.type = 'revenue_wise'

    @api.onchange('revenue_wise')
    def _onchange_revenue_wise(self):
        """for changing the selection the data also delete for the previous selection for field revenue wise"""
        self.revenue_wise_ids.unlink()
        self.type = 'revenue_wise'

    @api.constrains('start_date', 'end_date')
    def _check_duration(self):
        """checking Start Date is after End Date"""
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise UserError("Start Date cannot be after End Date")

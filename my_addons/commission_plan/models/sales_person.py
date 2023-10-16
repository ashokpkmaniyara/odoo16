# -*- coding: utf-8 -*-
from odoo import fields, models


class SalesTeam(models.Model):
    """class for inheriting res.users for adding a field"""

    _inherit = 'res.users'

    commission_plan_id = fields.Many2one('crm.commission', string='Commission Plan', help='specify a plan')

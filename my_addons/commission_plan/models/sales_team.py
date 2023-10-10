# -*- coding: utf-8 -*-
from odoo import fields, models


class SalesTeam(models.Model):
    _inherit = 'crm.team'

    commission_plan_id = fields.Many2one('crm.commission', string='Commission Plan')
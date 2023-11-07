# -*- coding: utf-8 -*-
from odoo import models, fields


class AddField(models.Model):
    _inherit = 'project.project'

    S_date = fields.One2many('')
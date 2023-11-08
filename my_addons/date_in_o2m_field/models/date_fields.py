# -*- coding: utf-8 -*-
from odoo import models, fields


class DateFields(models.Model):
    _name = 'date.fields'
    _description = 'Date fields'

    month = fields.Selection([
        ('1', 'January'),
        ('2', 'February'),
        ('3', 'March'),
        ('4', 'April'),
        ('5', 'May'),
        ('6', 'June'),
        ('7', 'July'),
        ('8', 'August'),
        ('9', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December')
    ], string="Month", required=1)
    year = fields.Char(string='Year', help='specify the year',rquired=1)
    from_date = fields.Date(string='From Date', help='select the starting date')
    to_date = fields.Date(string='To Date', help='select the end date')
    o2m_field_id = fields.Many2one('project.project')

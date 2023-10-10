# -*- coding: utf-8 -*-

from odoo import fields, models


class EventType(models.Model):
    """class for event type"""
    _name = "event.type"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Event Type"

    name = fields.Char(required=1, string="Name")
    code = fields.Char(required=1, string="Code")
    image = fields.Image(string="Image", type="base64", attachment=0)
    type_ids = fields.One2many("event.booking", "event_type_id", "Event Type")

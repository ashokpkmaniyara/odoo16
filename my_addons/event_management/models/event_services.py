# -*- coding: utf-8 -*-

from odoo import fields, models, api


class EventServices(models.Model):
    """class for event services"""
    _name = "event.services"
    _description = "Event services"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=1)
    responsible_person_id = fields.Many2one("res.users", "Responsible Person", required=1,
                                            default=lambda self: self.env.user)
    child_ids = fields.One2many("event.services.tree", "parent_id", string="Service Line")


class EventServicesTree(models.Model):
    """child class of event services"""
    _name = "event.services.tree"
    _description = "Event Services Tree"

    description = fields.Char()
    quantity = fields.Integer(default=1)
    unit_price = fields.Float()
    subtotal = fields.Float(compute="_compute_subtotal", options="{'currency_field': 'company_currency'}")
    currency_id = fields.Many2one("res.currency", string='Currency',
                                  default=lambda self: self.env.user.company_id.currency_id)
    parent_id = fields.Many2one("event.services", string="Parent")

    @api.depends("quantity", "unit_price")
    def _compute_subtotal(self):
        """To get the total price per line"""
        for record in self:
            record.subtotal = record.quantity * record.unit_price

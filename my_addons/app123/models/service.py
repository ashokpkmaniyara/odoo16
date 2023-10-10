# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Service(models.Model):
    _name = 'manage.service'

    name = fields.Char(string='Name', required=1)
    responsible_person_id = fields.Many2one("res.users", string='Responsible Person',
                                            default=lambda self: self.env.user)
    service_ids = fields.One2many("service.tree", "tree_id", "service")


class ServiceTree(models.Model):
    _name = 'service.tree'

    description = fields.Char(string='Description')
    quantity = fields.Integer(string='Quantity', default=1)
    unit_price = fields.Float(string='Price')
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal')
    tree_id = fields.Many2one("manage.service", string='tree')

    @api.depends("unit_price", "quantity")
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.quantity * rec.unit_price

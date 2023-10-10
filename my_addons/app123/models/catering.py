# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Catering(models.Model):
    _name = 'manage.catering'

    name = fields.Char(readonly=1)
    event_id = fields.Many2one(string='Event', comodel_name='manage.booking', required=1)
    date = fields.Date(string='Date', related='event_id.booking_date')
    start_date = fields.Date(string='Start date', related='event_id.start_date')
    end_date = fields.Date(string='End Date', related='event_id.end_date')
    guests = fields.Integer(string='Guests', default=1)
    welcome_drink = fields.Boolean(string="Welcome Drink")
    breakfast = fields.Boolean(string="Breakfast")
    lunch = fields.Boolean(string="Lunch")
    dinner = fields.Boolean(string="Dinner")
    snacks_and_drinks = fields.Boolean(string="Snacks & Drinks")
    beverages = fields.Boolean(string="Beverages")
    welcome_drink_ids = fields.One2many("catering.page", inverse_name="welcome_drink_id")
    breakfast_ids = fields.One2many("catering.page", inverse_name="breakfast_id")
    lunch_ids = fields.One2many("catering.page", inverse_name="lunch_id")
    dinner_ids = fields.One2many("catering.page", inverse_name="dinner_id")
    snacks_and_drinks_ids = fields.One2many("catering.page", inverse_name="snacks_and_drinks_id")
    beverages_ids = fields.One2many("catering.page", inverse_name="beverages_id")
    grand_total = fields.Float(compute='_compute_grand_total')
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('delivered', 'Delivered'),
        ('invoiced', 'Invoiced'),
        ('expired', 'Expired')
    ], string='Status', required=True, readonly=True, copy=False,
        tracking=True, default='draft')

    @api.model
    def create(self, vals):
        """to generate sequence name"""
        vals['name'] = self.env['ir.sequence'].next_by_code('sequence_catering')
        catering = super(Catering, self).create(vals)

        if 'event_id' in vals:
            event = self.env['manage.booking'].browse(vals['event_id'])
            event.write({
                'catering_creation': True
            })
        return catering

    @api.depends("welcome_drink_ids", "breakfast_ids", "lunch_ids", "dinner_ids",
                 "snacks_and_drinks_ids", "beverages_ids")
    def _compute_grand_total(self):
        for rec in self:
            total_welcome_drink = rec.welcome_drink_ids.mapped(lambda total: total.subtotal)
            total_breakfast = rec.breakfast_ids.mapped(lambda total: total.subtotal)
            total_lunch = rec.lunch_ids.mapped(lambda total: total.subtotal)
            total_dinner = rec.dinner_ids.mapped(lambda total: total.subtotal)
            total_snacks_and_drinks = rec.snacks_and_drinks_ids.mapped(lambda total: total.subtotal)
            total_beverages = rec.beverages_ids.mapped(lambda total: total.subtotal)

            total_sum = sum(
                total_welcome_drink + total_breakfast + total_lunch + total_dinner + total_snacks_and_drinks + total_beverages)
            rec.grand_total = total_sum

    def expired(self):
        """function to change the state to expired"""
        today = fields.Date.today()
        expired_records = self.search([('start_date', '<', today)])
        expired_records.write({'state': 'expired'})

    def button_confirm(self):
        self.state = "confirmed"
        self.event_id.state = "confirmed"

    def button_delivered(self):
        self.state = "delivered"
        self.event_id.state = "delivered"


class CateringPage(models.Model):
    _name = 'catering.page'

    welcome_drink_id = fields.Many2one("manage.catering", "Welcome Drink", readonly=1)
    breakfast_id = fields.Many2one("manage.catering", "Breakfast", readonly=1)
    lunch_id = fields.Many2one("manage.catering", "Lunch", readonly=1)
    dinner_id = fields.Many2one("manage.catering", "Dinner", readonly=1)
    snacks_and_drinks_id = fields.Many2one("manage.catering", "Snacks and Drinks", readonly=1)
    beverages_id = fields.Many2one("manage.catering", "Beverages", readonly=1)
    item_id = fields.Many2one("manage.menu", string="Item", required=1)
    description = fields.Char(string="Description")
    quantity = fields.Integer(string="Quantity", default=1)
    uom_id = fields.Many2one(string="UOM",
                             related="item_id.uom_id")
    unit_price_id = fields.Float(string="Unit Price",
                                 related="item_id.unit_price")
    subtotal = fields.Float(string="Subtotal", compute="_compute_subtotal", store=1)

    @api.depends("unit_price_id", "quantity")
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.quantity * rec.unit_price_id

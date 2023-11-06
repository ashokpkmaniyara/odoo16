# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions


class EventCatering(models.Model):
    """class for event catering, here all the fields are defined"""
    _name = "event.catering"
    _description = "Event Catering"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(readonly=1)
    catering_event_id = fields.Many2one("event.booking", "Event", required=1,
                                        domain="[('booking_state', 'in', ['draft'])]")
    catering_date = fields.Date(string="Date",
                                related="catering_event_id.booking_date")
    catering_start_date = fields.Date(string="Start Date",
                                      related="catering_event_id.event_start_date",
                                      store=1)
    catering_end_date = fields.Date(string="End Date",
                                    related="catering_event_id.event_end_date")
    catering_guests = fields.Integer(string="Guests", default=1)
    catering_welcome_drink = fields.Boolean(string="Welcome Drink")
    catering_breakfast = fields.Boolean(string="Breakfast")
    catering_lunch = fields.Boolean(string="Lunch")
    catering_dinner = fields.Boolean(string="Dinner")
    catering_snacks_and_drinks = fields.Boolean(string="Snacks & Drinks")
    catering_beverages = fields.Boolean(string="Beverages")
    child_welcome_drink_ids = fields.One2many("event.catering.pages",
                                              inverse_name="parent_welcome_drink_id")
    child_breakfast_ids = fields.One2many("event.catering.pages",
                                          inverse_name="parent_breakfast_id")
    child_lunch_ids = fields.One2many("event.catering.pages",
                                      inverse_name="parent_lunch_id")
    child_dinner_ids = fields.One2many("event.catering.pages",
                                       inverse_name="parent_dinner_id")
    child_snacks_and_drinks_ids = fields.One2many("event.catering.pages",
                                                  inverse_name="parent_snacks_and_drinks_id")
    child_beverages_ids = fields.One2many("event.catering.pages",
                                          inverse_name="parent_beverages_id")
    catering_state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('delivered', 'Delivered'),
        ('invoiced', 'Invoiced'),
        ('expired', 'Expired')
    ], string="State", default="draft", tracking=1)

    catering_grand_total = fields.Float("Grand Total",
                                        compute="_compute_grand_total",
                                        options="{'currency_field': 'company_currency'}",
                                        store=True)
    currency_id = fields.Many2one("res.currency", string='Currency',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id)

    @api.depends('child_welcome_drink_ids', 'child_breakfast_ids',
                 'child_lunch_ids', 'child_dinner_ids',
                 'child_snacks_and_drinks_ids', 'child_beverages_ids')
    def _compute_grand_total(self):
        """function to calculate the total amount of all the pages in the notebook"""
        for i in self:
            total_list_welcome_drink = i.child_welcome_drink_ids.mapped(
                lambda
                    subtotal_record: subtotal_record.event_catering_page_subtotal)
            total_list_breakfast = i.child_breakfast_ids.mapped(
                lambda
                    subtotal_record: subtotal_record.event_catering_page_subtotal)
            total_list_lunch = i.child_lunch_ids.mapped(
                lambda
                    subtotal_record: subtotal_record.event_catering_page_subtotal)
            total_list_dinner = i.child_dinner_ids.mapped(
                lambda
                    subtotal_record: subtotal_record.event_catering_page_subtotal)
            total_list_snacks_and_drinks = i.child_snacks_and_drinks_ids.mapped(
                lambda
                    subtotal_record: subtotal_record.event_catering_page_subtotal)
            total_list_beverages = i.child_beverages_ids.mapped(
                lambda
                    subtotal_record: subtotal_record.event_catering_page_subtotal)

            total_sum = sum(
                total_list_welcome_drink + total_list_breakfast + total_list_lunch + total_list_dinner +
                total_list_snacks_and_drinks + total_list_beverages)
            i.catering_grand_total = total_sum

    @api.model
    def create(self, vals):
        """to generate sequence name"""
        vals['name'] = self.env['ir.sequence'].next_by_code('sequence_catering')
        catering = super().create(vals)
        if 'catering_event_id' in vals:
            event = self.env['event.booking'].browse(vals['catering_event_id'])
            event.write({
                'catering_creation': True
            })
        return catering

    def button_confirmed(self):
        """button to change the state from draft to confirmed"""
        self.write({'catering_state': "confirmed"})
        self.catering_event_id.booking_state = "confirmed"

    def button_delivered(self):
        """button to change the state from confirm to delivered"""
        self.write({'catering_state': "delivered"})
        self.catering_event_id.booking_state = "delivered"

    def expired(self):
        """function to change the state to expired"""
        today = fields.Date.today()
        expired_records = self.search([('catering_start_date', '<', today)])
        expired_records.write({'catering_state': 'expired'})

    @api.constrains('child_welcome_drink_ids', 'child_breakfast_ids',
                    'child_lunch_ids',
                    'child_dinner_ids', 'child_snacks_and_drinks_ids',
                    'child_beverages_ids', 'catering_state')
    def _check_selected_pages(self):
        """to check at least 1 page is selected before saving otherwise raise
        exception"""
        for catering in self:
            if catering.catering_state in ['draft']:
                if not (
                        catering.child_welcome_drink_ids or catering.child_breakfast_ids
                        or catering.child_lunch_ids or catering.child_dinner_ids
                        or catering.child_snacks_and_drinks_ids or catering.child_beverages_ids):
                    raise exceptions.ValidationError(
                        "You must select at least one item.")

    @api.onchange('catering_welcome_drink')
    def _onchange_catering_welcome_drink(self):
        """Delete related 'Welcome Drink' pages when 'Welcome Drink' is unticked."""
        if not self.catering_welcome_drink:
            self.child_welcome_drink_ids.unlink()
            self.catering_welcome_drink = False

    @api.onchange('catering_breakfast')
    def _onchange_catering_breakfast(self):
        """Delete related 'Breakfast' pages when 'Breakfast' is unticked."""
        if not self.catering_breakfast:
            self.child_breakfast_ids.unlink()
            self.catering_breakfast = False

    @api.onchange('catering_lunch')
    def _onchange_catering_lunch(self):
        """Delete related 'Lunch' pages when 'Lunch' is unticked."""
        if not self.catering_lunch:
            self.child_lunch_ids.unlink()
            self.catering_lunch = False

    @api.onchange('catering_dinner')
    def _onchange_catering_dinner(self):
        """Delete related 'Dinner' pages when 'Dinner' is unticked."""
        if not self.catering_dinner:
            self.child_dinner_ids.unlink()
            self.catering_dinner = False

    @api.onchange('catering_snacks_and_drinks')
    def _onchange_catering_snacks_and_drinks(self):
        """Delete related 'Snacks and Drinks' pages when 'Snacks and Drinks' is unticked."""
        if not self.catering_snacks_and_drinks:
            self.child_snacks_and_drinks_ids.unlink()
            self.catering_snacks_and_drinks = False

    @api.onchange('catering_beverages')
    def _onchange_catering_lunch(self):
        """Delete related 'Beverages' pages when 'Beverages' is unticked."""
        if not self.catering_beverages:
            self.child_beverages_ids.unlink()
            self.catering_beverages = False


class EventCateringPages(models.Model):
    """model for event catering pages with fields fetching from event catering page"""
    _name = "event.catering.pages"
    _description = "Event Catering Page"

    parent_welcome_drink_id = fields.Many2one("event.catering", "Welcome Drink",
                                              readonly=1)
    parent_breakfast_id = fields.Many2one("event.catering", "Breakfast",
                                          readonly=1)
    parent_lunch_id = fields.Many2one("event.catering", "Lunch", readonly=1)
    parent_dinner_id = fields.Many2one("event.catering", "Dinner", readonly=1)
    parent_snacks_and_drinks_id = fields.Many2one("event.catering",
                                                  "Snacks and Drinks",
                                                  readonly=1)
    parent_beverages_id = fields.Many2one("event.catering", "Beverages",
                                          readonly=1)
    event_catering_page_item_id = fields.Many2one("event.catering.type",
                                                  string="Item", required=1)
    event_catering_page_description = fields.Char(string="Description")
    event_catering_page_quantity = fields.Integer(string="Quantity", default=1)
    event_catering_page_uom_id = fields.Many2one(string="UOM",
                                                 related="event_catering_page_item_id.catering_type_uom_id")
    event_catering_page_unit_price_id = fields.Float(string="Unit Price",
                                                     related="event_catering_page_item_id.catering_type_unit_price")
    event_catering_page_subtotal = fields.Float(string="Subtotal",
                                                compute="_compute_subtotal",
                                                store=1)
    parent_id = fields.Many2one("event.catering", "parent")
    currency_id = fields.Many2one("res.currency", string='Currency')

    @api.depends("event_catering_page_unit_price_id",
                 "event_catering_page_quantity")
    def _compute_subtotal(self):
        """function to compute the subtotal with price and quantity"""
        for record in self:
            record.event_catering_page_subtotal = (
                        record.event_catering_page_unit_price_id *
                        record.event_catering_page_quantity)

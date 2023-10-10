# -*- coding: utf-8 -*-

from odoo import models, fields


class EventCateringType(models.Model):
    """class for the catering types and here specify the fields"""
    _name = "event.catering.type"
    _description = "Event Catering Type"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "catering_type_name"

    catering_type_name = fields.Char(string="Name", required=1)
    catering_type_category = fields.Selection(
        selection=[('welcome_drink', 'Welcome Drink'), ('breakfast', 'Breakfast'), ('lunch', 'Lunch'),
                   ('dinner', 'Dinner'), ('snacks_and_drinks', 'Snacks and Drinks'), ('beverages', 'Beverages')],
        string="Category", required=1)
    catering_type_image = fields.Image(string="Image", type="base64", attachment=0)
    catering_type_uom_id = fields.Many2one("uom.uom", string="UOM", required=1,
                                           default=lambda self: self.env['uom.uom'].search([('name', '=', 'Units')]))
    catering_type_unit_price = fields.Float(string="Unit Price", required=1)

    catering_type_item_ids = fields.One2many("event.catering.pages", "event_catering_page_item_id", string="Catering "
                                                                                                           "Pages")

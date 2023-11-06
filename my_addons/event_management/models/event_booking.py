# -*- coding: utf-8 -*-


from odoo import api, fields, models, _
from odoo.exceptions import UserError


class EventBooking(models.Model):
    """class for event booking"""
    _name = "event.booking"
    _description = "Event Booking"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "sequence_name"

    sequence_name = fields.Char(readonly=1)
    name = fields.Char(string="Name", compute="_compute_name")
    event_type_id = fields.Many2one("event.type", string="Event Type",
                                    required=1)

    booking_date = fields.Date(default=fields.Datetime.now(), required=1)
    event_start_date = fields.Date(default=fields.Datetime.now(),
                                   string="Start Date", required=1)
    event_end_date = fields.Date(string="End Date", required=1)
    time_duration = fields.Integer(compute="_compute_duration")
    partner_id = fields.Many2one("res.partner", "Partner", required=1)
    partner_invoice_id = fields.Many2one("res.partner_invoice",
                                         "Partner Invoice")
    partner_shipping_id = fields.Many2one("res.partner_09/20/2023shipping",
                                          "Partner Shipping")
    catering_ids = fields.One2many("event.catering", "catering_event_id")
    booking_state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('delivered', 'Delivered'),
        ('invoiced', 'Invoiced'),
        ('expired', 'Expired')
    ], string="State", default="draft",tracking=1)
    record_count = fields.Integer(compute="_compute_record_count")
    cat_id = fields.Many2one("event.catering.pages", invisible="1")
    catering_creation = fields.Boolean()
    invoice_id = fields.Many2one(comodel_name='account.move')
    is_paid = fields.Boolean(string="Paid", default=False)

    @api.depends("catering_ids.catering_event_id")
    def _compute_record_count(self):
        """to find the count of the records created for event booking"""
        for record in self:
            record.record_count = len(record.catering_ids.catering_event_id)

    @api.model
    def create(self, vals):
        """to generate sequence name"""
        vals['sequence_name'] = self.env['ir.sequence'].next_by_code(
            'sequence_booking')
        return super(EventBooking, self).create(vals)

    def button_confirm(self):
        """confirm button for event booking to change state from draft to confirm"""
        self.booking_state = "confirmed"
        self.catering_ids.catering_state = "confirmed"

    def button_delivered(self):
        """delivered button for event booking to change state from confirm to delivered"""
        self.booking_state = "delivered"
        self.catering_ids.catering_state = "delivered"

    @api.constrains('event_start_date', 'event_end_date')
    def _check_duration(self):
        """checking Start Date is after End Date"""
        if self.event_start_date and self.event_end_date and self.event_start_date > self.event_end_date:
            raise UserError("Start Date cannot be after End Date")

    @api.depends('event_start_date', 'event_end_date')
    def _compute_duration(self):
        """duration calculation using start date and end date"""

        for record in self:
            if record.event_start_date and record.event_end_date and record.event_start_date < record.event_end_date:
                record.time_duration = (
                            record.event_end_date - record.event_start_date).days
            elif record.event_start_date == record.event_end_date:
                record.time_duration = 1
            else:
                record.time_duration = 0

    @api.depends('event_type_id', 'partner_id.name', 'event_start_date',
                 'event_end_date')
    def _compute_name(self):
        for record in self:
            if record.event_type_id and record.partner_id and record.event_start_date and record.event_end_date:
                record.name = (str(record.event_type_id.name) +
                               ":" + str(record.partner_id.name) +
                               "/" + str(record.event_start_date) + ":"
                               + str(record.event_end_date))
            else:
                record.name = "New"

    def button_catering(self):
        """button to go to new page with pre-filled data"""
        self.write({'booking_state': "draft"})
        return {'name': _('Event Catering'),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'event.catering',
                'view_id': False,
                'type': 'ir.actions.act_window',

                'context': {'default_catering_event_id': self.id,
                            'default_catering_date': self.booking_date,
                            'default_catering_start_date': self.event_start_date,
                            'default_catering_end_date': self.event_end_date}}

    def button_invoiced(self):
        """button to create invoice"""
        self.booking_state = "invoiced"
        self.catering_ids.catering_state = "invoiced"

        invoice_lines = []

        for catering_type in ['welcome_drink', 'breakfast', 'lunch', 'dinner',
                              'snacks_and_drinks', 'beverages']:
            for product in getattr(self.catering_ids,
                                   f'child_{catering_type}_ids'):
                invoice_line = fields.Command.create({
                    'product_id': '',
                    'name': product.event_catering_page_item_id.catering_type_name,
                    'quantity': product.event_catering_page_quantity,
                    'price_unit': product.event_catering_page_unit_price_id,
                    'price_subtotal': product.event_catering_page_subtotal,
                })
                invoice_lines.append(invoice_line)

        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'invoice_date': self.booking_date,
            'partner_id': self.partner_id.id,
            'event_type': self.event_type_id.name,
            'duration': self.time_duration,
            'invoice_line_ids': invoice_lines,
        })

        self.is_paid = True
        self.invoice_id = invoice.id
        invoice.action_post()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': invoice.id,
            'target': 'current',
        }

    def catering_smart_button(self):
        """smart button to show the created catering service"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Event',
            'view_mode': 'form',
            'res_model': 'event.catering',
            'res_id': self.env['event.catering'].search(
                [('catering_event_id', '=', self.id)]).id,
            'context': {'create': False}
        }

    def invoice_smart_button(self):
        """smart button to show created invoice"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': self.invoice_id.id,
            'target': 'current',
        }

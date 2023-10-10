

from odoo import models, fields, api


class ManageBooking(models.Model):
    _name = "manage.booking"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', compute='_compute_name')
    type_id = fields.Many2one("manage.type", string='Type')
    customer_id = fields.Many2one("res.partner", string='Customer')
    partner_invoice_id = fields.Many2one("res.partner_invoice", "Partner Invoice")
    partner_shipping_id = fields.Many2one("res.partner_09/20/2023shipping", "Partner Shipping")
    booking_date = fields.Date(string='Booking Date')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    duration = fields.Integer(string='Duration', compute='_compute_duration')
    catering_creation = fields.Boolean(invisible=1)
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('delivered', 'Delivered'),
        ('invoiced', 'Invoiced'),
        ('expired', 'Expired')
    ], string='Status', required=True, readonly=True, copy=False,
        tracking=True, default='draft')

    @api.depends("start_date", "end_date")
    def _compute_duration(self):
        for rec in self:
            if rec.start_date and rec.end_date and rec.end_date > rec.start_date:
                rec.duration = (rec.end_date - rec.start_date).days
            else:
                rec.duration = 0

    @api.depends('type_id', 'customer_id.name', 'start_date', 'end_date')
    def _compute_name(self):
        """sequence name from the input details"""
        for record in self:
            type = record.type_id.name or ''
            name = record.customer_id.name.split(' ')[0] if record.customer_id else ''
            start = record.start_date.strftime('%d-%m-%Y') if record.start_date else ''
            end = record.end_date.strftime('%d-%m-%Y') if record.end_date else ''

            if type and name and start and end:
                record.name = f"{type} : {name} / {start}:{end}"
            else:
                record.name = f"{type} {name} {start} {end}"

    def button_catering(self):
        self.write({'state': "draft"})
        return {'name': 'Catering',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'manage.catering',
                'view_id': False,
                'type': 'ir.actions.act_window',

                'context': {'default_event_id': self.id,
                            'default_date': self.booking_date,
                            'default_start_date': self.start_date,
                            'default_end_date': self.end_date}}

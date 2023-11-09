from datetime import timedelta

from odoo import fields, models, api


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate_property"

    name = fields.Char(required=1)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=fields.Datetime.now() + timedelta(days=3 * 30), copy=False)
    expected_price = fields.Float()
    selling_price = fields.Float(default=100, readonly=1, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Float()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Float()
    active = fields.Boolean(default=1)
    garden_orientation = fields.Selection(
        string='Type',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'),
                   ('west', 'West')],
        help="Type is used to select North’, ‘South’, ‘East’ and ‘West’")
    state = fields.Selection(string='Status',
                             selection=[('new', 'New'),
                                        ('offer received', 'Offer received'),
                                        ('offer accepted', 'Offer accepted'),
                                        ('sold', 'Sold'),
                                        ('canceled', 'Canceled')],
                             default='new', copy=False)
    property_type = fields.Many2one("property.type", string="Property_type")
    partner_id = fields.Many2one("res.partner", string="Buyer", copy=0)
    user_id = fields.Many2one("res.users", string="Seller",
                              default=lambda self: self.env.user)
    tag_ids = fields.Many2many("property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for area in self:
            area.total_area = area.living_area + area.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for best in self:
            if best.offer_ids:
                best.best_price = max(best.offer_ids.mapped("price"))
            else:
                best.best_price = 0.00

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = None
            self.garden_orientation = None

    def action_sold(self):
        print("Button")


class PropertyTypes(models.Model):
    _name = "property.type"
    _description = "property_type"

    name = fields.Char(required=1)


class PropertyTags(models.Model):
    _name = "property.tag"
    _description = "property_tag"

    name = fields.Char(required=1)


class PropertyOffer(models.Model):
    _name = "estate.property.offer"

    price = fields.Float()
    status = fields.Selection(string="Status",
                              selection=[('accepted', 'Accepted'),
                                         ('refused', 'Refused')], copy=0)
    partner_id = fields.Many2one("res.partner", "Partner", required=1)
    property_id = fields.Many2one("estate.property", required=1)
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline",
                                inverse="_compute_validity")

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(
                    days=record.validity)

    def _compute_validity(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (
                            record.date_deadline - record.create_date.date()).days

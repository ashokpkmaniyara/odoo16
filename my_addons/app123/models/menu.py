from odoo import models, fields


class Menu(models.Model):
    _name = 'manage.menu'

    name = fields.Char(string="Name", required=1)
    category = fields.Selection(
        selection=[('welcome_drink', 'Welcome Drink'), ('breakfast', 'Breakfast'), ('lunch', 'Lunch'),
                   ('dinner', 'Dinner'), ('snacks_and_drinks', 'Snacks and Drinks'), ('beverages', 'Beverages')],
        string="Category", required=1)
    image = fields.Image(string="Image", type="base64", attachment=0)
    uom_id = fields.Many2one("uom.uom", string="UOM", required=1,
                             default=lambda self: self.env['uom.uom'].search([('name', '=', 'Units')]))
    unit_price = fields.Float(string="Unit Price", required=1)
    # menu_ids = fields.One2many("catering.page","item_id")

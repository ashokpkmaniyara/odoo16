# -*- coding: utf-8 -*-

from odoo import models, fields


class Type(models.Model):
    _name = 'manage.type'

    name = fields.Char(string='Name')
    code = fields.Integer(string="Code")
    image = fields.Image(string='Image', type="base64", attachment=0)

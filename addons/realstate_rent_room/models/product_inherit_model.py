# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class ProductInherit(models.Model):
    _inherit = "product.product"

    place_id = fields.Many2one(
        comodel_name="realstate_rent_room.rent_place"
    )
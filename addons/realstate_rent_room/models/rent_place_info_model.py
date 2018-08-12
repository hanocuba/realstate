# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class RentPlaceInfo(models.Model):
    _name = "realstate_rent_room.rent_place_info"

    name = fields.Many2one(
        comodel_name='realstate_rent_room.rent_place_info_key'
    )

    value = fields.Char(
        string="Valor"
    )

    rent_place_id = fields.Many2one(
        comodel_name="realstate_rent_room.rent_place"
    )

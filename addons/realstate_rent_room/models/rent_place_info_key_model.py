# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class RentPlaceInfoKey(models.Model):
    _name = "realstate_rent_room.rent_place_info_key"

    name = fields.Char(
        string=u'Característica'
    )

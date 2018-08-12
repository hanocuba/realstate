# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class RentPlaceLike(models.Model):
    _name = 'realstate_rent_room.rent_place_like'

    like = fields.Boolean()

    place_id = fields.Many2one(
        comodel_name='realstate_rent_room.rent_place'
    )

    user_id = fields.Many2one(
        comodel_name='res.users'
    )

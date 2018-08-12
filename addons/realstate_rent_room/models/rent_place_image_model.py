# -*- coding: utf-8 -*-
# /**************************************************************************
# **   CODE LICENCE
# **   Developer: Dairon Domínguez Vega
# **   Date: 12/2/16
# **************************************************************************/
# /*                               __
#  *                            | /  \ |
#  *                           \_\\  //_/
#  *                            .'/()\'.
#  *                             \\  //
#  *
#  *    _/_/_/              _/
#  *   _/    _/    _/_/_/      _/  _/_/    _/_/    _/_/_/
#  *  _/    _/  _/    _/  _/  _/_/      _/    _/  _/    _/
#  * _/    _/  _/    _/  _/  _/        _/    _/  _/    _/
#  *_/_/_/      _/_/_/  _/  _/          _/_/    _/    _/
#  *
#  *
from odoo import models, fields, api
from odoo import tools, _


class ImageMemo(models.Model):
    _name = 'realstate_rent_room.rent_place_image'

    name = fields.Char(string='Nombre')
    image = fields.Binary(string='Fichero')
    rent_place_id = fields.Many2one(comodel_name='realstate_rent_room.rent_place')
    description = fields.Text(string=u'Descripción')
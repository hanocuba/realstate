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


class Marker(models.Model):
    _name = 'map_leaft.marker'

    name = fields.Char(string='Nombre')
    map_id = fields.Many2one(comodel_name='map_leaft.map')

    lat = fields.Float(string='Latitud')
    lon = fields.Float(string='Longitud')

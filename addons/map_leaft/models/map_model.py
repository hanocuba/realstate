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


class Map(models.Model):
    _name = 'map_leaft.map'

    name = fields.Char(string=u'Descripción')

    config_json = fields.Char(string='Configuración JSON')
    marker_id = fields.One2many(comodel_name='map_leaft.marker', inverse_name='map_id',
                                string='Marcadores')


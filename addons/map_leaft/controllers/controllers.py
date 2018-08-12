# -*- coding: utf-8 -*-
from odoo import http

# class MapLeaft(http.Controller):
#     @http.route('/map_leaft/map_leaft/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/map_leaft/map_leaft/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('map_leaft.listing', {
#             'root': '/map_leaft/map_leaft',
#             'objects': http.request.env['map_leaft.map_leaft'].search([]),
#         })

#     @http.route('/map_leaft/map_leaft/objects/<model("map_leaft.map_leaft"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('map_leaft.object', {
#             'object': obj
#         })
# -*- coding: utf-8 -*-
from odoo import http

# class RealstateRentRoom(http.Controller):
#     @http.route('/realstate_rent_room/realstate_rent_room/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/realstate_rent_room/realstate_rent_room/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('realstate_rent_room.listing', {
#             'root': '/realstate_rent_room/realstate_rent_room',
#             'objects': http.request.env['realstate_rent_room.realstate_rent_room'].search([]),
#         })

#     @http.route('/realstate_rent_room/realstate_rent_room/objects/<model("realstate_rent_room.realstate_rent_room"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('realstate_rent_room.object', {
#             'object': obj
#         })
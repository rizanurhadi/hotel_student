# -*- coding: utf-8 -*-
from odoo import http

# class HotelBuilding(http.Controller):
#     @http.route('/hotel_building/hotel_building/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hotel_building/hotel_building/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hotel_building.listing', {
#             'root': '/hotel_building/hotel_building',
#             'objects': http.request.env['hotel_building.hotel_building'].search([]),
#         })

#     @http.route('/hotel_building/hotel_building/objects/<model("hotel_building.hotel_building"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hotel_building.object', {
#             'object': obj
#         })
# -*- coding: utf-8 -*-
# from odoo import http


# class OpenacademyStarly(http.Controller):
#     @http.route('/openacademy_starly/openacademy_starly/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/openacademy_starly/openacademy_starly/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('openacademy_starly.listing', {
#             'root': '/openacademy_starly/openacademy_starly',
#             'objects': http.request.env['openacademy_starly.openacademy_starly'].search([]),
#         })

#     @http.route('/openacademy_starly/openacademy_starly/objects/<model("openacademy_starly.openacademy_starly"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('openacademy_starly.object', {
#             'object': obj
#         })

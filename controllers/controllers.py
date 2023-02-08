# -*- coding: utf-8 -*-
# from odoo import http


# class Plaiaundi(http.Controller):
#     @http.route('/plaiaundi/plaiaundi', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/plaiaundi/plaiaundi/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('plaiaundi.listing', {
#             'root': '/plaiaundi/plaiaundi',
#             'objects': http.request.env['plaiaundi.plaiaundi'].search([]),
#         })

#     @http.route('/plaiaundi/plaiaundi/objects/<model("plaiaundi.plaiaundi"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('plaiaundi.object', {
#             'object': obj
#         })

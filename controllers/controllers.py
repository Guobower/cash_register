# -*- coding: utf-8 -*-
from odoo import http

# class CashRegister(http.Controller):
#     @http.route('/cash_register/cash_register/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cash_register/cash_register/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cash_register.listing', {
#             'root': '/cash_register/cash_register',
#             'objects': http.request.env['cash_register.cash_register'].search([]),
#         })

#     @http.route('/cash_register/cash_register/objects/<model("cash_register.cash_register"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cash_register.object', {
#             'object': obj
#         })
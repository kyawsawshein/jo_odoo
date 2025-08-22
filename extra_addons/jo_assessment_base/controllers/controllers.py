# -*- coding: utf-8 -*-
# from odoo import http


# class JoAssessmentBase(http.Controller):
#     @http.route('/jo_assessment_base/jo_assessment_base', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/jo_assessment_base/jo_assessment_base/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('jo_assessment_base.listing', {
#             'root': '/jo_assessment_base/jo_assessment_base',
#             'objects': http.request.env['jo_assessment_base.jo_assessment_base'].search([]),
#         })

#     @http.route('/jo_assessment_base/jo_assessment_base/objects/<model("jo_assessment_base.jo_assessment_base"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('jo_assessment_base.object', {
#             'object': obj
#         })


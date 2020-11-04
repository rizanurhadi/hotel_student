# -*- coding: utf-8 -*-

from odoo import models, fields, api

class building(models.Model):
     _name = 'building'
     _description = 'Hotel Building'

     code = fields.Char(string='Code For Building')
     name = fields.Char(string='Building Name')
     location = fields.Text(string='Building Location')
     address = fields.Text(string='Building Address')
     status = fields.Boolean(string='Status',
                                 help='True when folio line created from \
                                 Reservation')


#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
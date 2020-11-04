# -*- coding: utf-8 -*-

from odoo import models, fields, api

class hotel_building(models.Model):
    _name = 'hotel_building.hotel_building'

    code = fields.Char(string='Code For Building',required=True)
    name = fields.Char(string='Building Name',required=True)
    location = fields.Text(string='Building Location')
    address = fields.Text(string='Building Address')
    status = fields.Boolean(string='Active')
    

class Units(models.Model):
    _name = 'hotel_building.units'
    
    unit_no = fields.Char(string='Unit No')
    building_id = fields.Many2one('hotel_building.hotel_building', 'Building ID')
    
    location = fields.Text(string='Unit Location')
    address = fields.Text(string='Unit Address')
    status = fields.Boolean(string='Active')

    @api.multi
    def name_get(self):
        res = []
        for field in self :
            res.append((field.id, '%s' % (field.unit_no)))
        return res
    
    @api.onchange('building_id')
    def onchange_building_id(self):
        if self.building_id :
            #print("============TESTTSTSTST====================")
            #print(self.building_asset_id.id)
            building_id = self.building_id.id
            building_obj = self.env['hotel_building.hotel_building'].search([('id','=',building_id)])
            self.location = building_obj.location
            self.address = building_obj.address
        

class UnitsRoom(models.Model):
    _name = 'hotel_building.rooms'

    units_id = fields.Many2one('hotel_building.units', 'Units ID')
    name = fields.Char(string='Room Name')
    rate = fields.Float(string='Room Rate')
    description = fields.Text(string='Description')
    vacant = fields.Text(string='Room Vacant')
    status = fields.Boolean(string='Status',
                                help='True False')

class Assets(models.Model):
    _name = 'hotel_building.assets'
    #building_id = fields.Many2one('hotel_building.hotel_building', 'Building ID')
    name = fields.Char(string='Assets Name')
    description = fields.Text(string='Description')
    #qty = fields.Integer(string='Quantity')

class BuildingAssets(models.Model):
    _name = 'hotel_building.building.assets'
    building_id = fields.Many2one('hotel_building.hotel_building', 'Building ID')
    asset_id = fields.Many2one('hotel_building.assets', 'Asset ID')
    qty = fields.Integer(string='Quantity')

    @api.multi
    def name_get(self):
        res = []
        for field in self :
            res.append((field.id, '%s %s' % (field.building_id.name, field.asset_id.name)))
        return res

class RoomAssets(models.Model):
    _name = 'hotel_building.rooms.assets'
    building_asset_id = fields.Many2one('hotel_building.building.assets', 'Building Assets ID')
    room_id = fields.Many2one('hotel_building.rooms', 'Rooms ID')
    qty_total_asset = fields.Integer(related = 'building_asset_id.qty', string='Total Quantity')
    qty = fields.Integer(string='Quantity')

    @api.multi
    def name_get(self):
        res = []
        for field in self :
            res.append((field.id, '%s %s' % (field.building_asset_id.building_id.name, field.building_asset_id.asset_id.name)))
        return res

    @api.model
    def create(self, vals):
        """
        Overrides orm create method.
        @param self: The object pointer
        @param vals: dictionary of fields value.
        @return: new record set for hotel folio.
        """
        res = super(RoomAssets, self).create(vals)
        if vals.get('building_asset_id'):
            building_asets = self.env['hotel_building.building.assets'].browse(vals.get('building_asset_id',self.building_asset_id.id))
            print("=================TEST====================")
            print(self.building_asset_id.id)
            print(building_asets.qty)
            building_asets.write({'qty': building_asets.qty - vals.get('qty')})
        return res

    @api.multi
    def write(self, vals):
        """
        Overrides orm create method.
        @param self: The object pointer
        @param vals: dictionary of fields value.
        @return: new record set for hotel folio.
        """
        # print('============RUNNING WRITE==============')
        # print(self._context)
        # building_asets = self.env['hotel_building.building.assets'].browse(vals.get('building_asset_id',self.building_asset_id.id))
        # print("=================TEST====================")
        # print(self.building_asset_id.id)
        # print(building_asets.qty)
        # building_asets.write({'qty': building_asets.qty - vals.get('qty')})
        return super(RoomAssets, self).write(vals)
    
    @api.onchange('building_asset_id')
    def onchange_room_id(self):
        result = []
        if self.building_asset_id :
            #print("============TESTTSTSTST====================")
            #print(self.building_asset_id.id)
            id_buildingasset = self.building_asset_id.id
            building_obj = self.env['hotel_building.building.assets'].search([('id','=',id_buildingasset)])
            units_obj = self.env['hotel_building.units'].search([('building_id', '=', building_obj.building_id.id)])
            for unit in units_obj:
                result.append((unit.id))
            self.room_id= self.env['hotel_building.rooms'].search([('units_id', 'in',result)])

        return {'domain': { 
            'room_id': [('units_id', 'in',result)]}} 
            #self.room_id =  {'room_id': ['units_id','in',units_ids]}
            #res['domain']['state_id'] = [('country_id', '=', self.country_id.id)]
            #print(units_ids)
        # else :
        #     self.room_id =  {}
       
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import time
import datetime
import calendar

class Student(models.Model):
    _name = 'student.student'

    name = fields.Char(string='Name of Student')
    race = fields.Char()
    religion = fields.Char()
    gender = fields.Char()
    birthdate = fields.Char()
    identification_number = fields.Char()
    chinese_name = fields.Char()
    mobile_phone = fields.Char()
    email = fields.Char()
    address = fields.Text()
    country = fields.Char()
    photo = fields.Char()
    status = fields.Boolean(string='Active')

class StudentType(models.Model):
    _name ='student.type'
    student_id = fields.Many2one('student.student', 'Student ID')
    name = fields.Char(string='Contact Type')
    group = fields.Char(string='Programme Group')
    status = fields.Char(string='Contact Status Remark')

class School(models.Model):
    _name = 'student.school'
    name = fields.Char(string="Name of school")
    address = fields.Char(string="School Address")
    

class StudentSchools(models.Model):
    _name = 'student.student.schools'
    _rec_name = 'school_name'

    partner_id = fields.Many2one('res.partner', 'Student', ondelete='cascade', index=True, domain=[('student', '=', True)], required=True)
    #school_id = fields.Many2one('student.school', string='School')
    #school_name = fields.Char(related='school_id.name', readonly=False)
    school_name = fields.Char(string="Name of School")
    type = fields.Selection(
        [('primary', 'Primary'),
         ('secondary', 'Secondary'),
         ('tertiary', 'Tertiary')
        ], string='Type of School')
    highest = fields.Char(string="Highest Level Passed")
    class_number = fields.Char(string="Class Number")
    form_teacher = fields.Char(string="Form Teacher")
    contact_number = fields.Char(string="Contact Number")
    qualification_type = fields.Selection(
        [('alevel', 'A Level'),
         ('olevel', 'O Level'),
         ('advanced_diploma', 'Advanced Diploma'),
         ('degree', 'Degree'),
         ('diploma', 'Diploma'),
         ('masters', 'Masters'),
         ('phd', 'Phd')
        ], string='Qualification Type')
    honors = fields.Selection(
        [('1st', '1st'),
         ('2nd', '2nd'),
         ('3rd', '3rd'),
         ('cumlaude', 'Cum Laude'),
         ('merit', 'Merit')
        ], string='Honors')
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    remarks = fields.Char(string="Remarks")

class StudentValidation(models.Model):
    _name = 'student.validation'
    #_rec_name = 'school_name'
    partner_id = fields.Many2one('res.partner', 'Validation', ondelete='cascade', index=True, domain=[('student', '=', True)], required=True)
    validation_type = fields.Selection(
        [('employment_pass', 'Employment Pass'),
         ('passport', 'Passport'),
         ('singapore_nirc_blue', 'Singapore NIRC (Blue)'),
         ('singapore_nirc_pink', 'Singapore NIRC (Pink)'),
         ('student_pass', 'Student Pass'),
         ('work_permit', 'Work Permit'),
         ('birth_certificate', 'Birth Certificate')
        ], string='Validation Type')
    validation_number = fields.Char(string="Validation Number")
    approval  = fields.Char(string="Approval")
    valid_from = fields.Date(string="Valid From")
    valid_to = fields.Date(string="Valid To")
    remarks = fields.Char(string="Remarks")

class StudentPayment(models.Model):
    _name = 'student.payment'
    partner_id = fields.Many2one('res.partner', 'Student', ondelete='cascade', index=True, domain=[('student', '=', True)], required=True)
    payment_type = fields.Selection(
        [('tenancy', 'Tenancy'),
         ('transport', 'Transport'),
         ('meal', 'Meal'),
         ('deposit', 'Deposit'),
         ('return', 'Return Deposit')
        ], string='Payment Type')
    tenancy_id = fields.Many2one('student.tenancy','Tenancy',)
    room_rate = fields.Float(string='Room Rate',related='tenancy_id.room_id.rate',readonly=True)
    period = fields.Date(string="Period")
    amount  = fields.Float(string="Amount")
    discount  = fields.Float(string="Discount")
    total  = fields.Float(string="Total Payment")
    description  = fields.Char(string="Description")
    posting_date  = fields.Date(string="Posting Date", default=time.strftime("%Y-%m-%d 12:00:00"))
    boarding_type = fields.Selection(string='state', related='tenancy_id.boarding_type')
    payment_method = fields.Selection(
        [('cash', 'Cash'),
         ('transfer', 'Transfer'),
         ('cheque', 'Cheque'),
         ('creditcard', 'Credit Card'),
         ('ibanking', 'I-Banking'),
         ('other', 'Other')
        ], string='Payment Method')
    status = fields.Selection(
        [('paid', 'Paid'),
         ('unpaid', 'Unpaid')
        ], string='Paid',default='unpaid')
    invoice_id = fields.Many2one('student.invoice', 'Invoice Payment')

    @api.onchange('partner_id')
    def onchange_partner_id(self): 
        if self.partner_id : 
            tenancy_obj = self.env['student.tenancy']
            student_tenancy = tenancy_obj.search([('partner_id', '=',self.partner_id.id)])
            if student_tenancy :
                self.tenancy_id = student_tenancy.id
            else :
                raise ValidationError(_('Student doesn\'t have tenancy'))

        if not self.partner_id :
             self.tenancy_id = None
    
    # @api.multi
    # def write(self, vals):
        
    #     # vals['id'] = self.id
    #     # vals['partner_id'] = self.partner_id.id
    #     print(self)
    #     print(vals)
    #     payment_model = super(StudentPayment, self).write(vals)
    #     return payment_model

class StudentTenancy(models.Model):
    _name = 'student.tenancy'
    partner_id = fields.Many2one('res.partner', 'Student Name', ondelete='cascade', index=True, domain=[('student', '=', True)], required=True)
    building_id = fields.Many2one('hotel_building.hotel_building', 'Building ID')
    units_id = fields.Many2one('hotel_building.units', 'Units ID')
    room_id = fields.Many2one('hotel_building.rooms', 'Room ID',required=True)
    checkin = fields.Date(string="Check In",required=True)
    checkout = fields.Date(string="Check Out",required=True)
    #order_id
    payment_ids = fields.One2many('student.payment', 'tenancy_id', 'Payment')
    my31list = []
    for my31 in range(1,32):
        my31list.append((my31, my31))
    termofpayment = fields.Selection(my31list)
    boarding_type = fields.Selection(
        [('full', 'Full'),
         ('half', 'Half'),
         ('tenancy', 'Tenancy')
        ], string='Boarding Type')
    boarding_cost = fields.Float('Boarding Cost')
    deposit_amount = fields.Float('Deposit Amount')

    @api.multi
    def name_get(self):
        res = []
        for field in self :
            res.append((field.id, '%s - %s %s' % (field.partner_id.name,field.building_id.name,field.room_id.name)))
        return res

    @api.onchange('building_id')
    def onchange_building_id(self):
        if not self.building_id:
            return {'domain': {'units_id': []}}
        id_building = None
        if self.building_id :
            id_building = self.building_id.id
        #if self.room_id
        self.room_id = None
        self.units_id = None
        return {'domain': { 
            'units_id': [('building_id', '=',id_building)]}} 
    
    @api.onchange('units_id')
    def onchange_units_id(self):
        if not self.units_id:
            return {'domain': {'room_id': []}}
        id_units = None
        if self.units_id :
            id_units = self.units_id.id
        #self.room_id = None
        return {'domain': { 
            'room_id': [('units_id', '=',id_units)]}} 
    
    @api.onchange('room_id')
    def onchange_room_id(self):
        if not self.room_id:
            self.boarding_cost = 0
        if self.room_id:
            # check if room already occupied
            # based on rules 1 student 1 tenancy
            tenancy_model = self.env['student.tenancy']
            tenancy_obj = tenancy_model.search([('room_id', '=',self.room_id.id)])
            if tenancy_obj.id : 
                raise ValidationError(_('Room Already Occupied'))
            else :
                room_rate = self.room_id.rate
                self.boarding_cost = room_rate
            #     self.room_id = self.room_id.id
            # return {'domain': { 
            #          'room_id': [('units_id', '=',room_obj.units_id),('room_id', '=',self.room_id.id) ]}} 

    
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if self.partner_id:
            tenancy_obj = self.env['student.tenancy']
            room_obj = tenancy_obj.search([('partner_id', '=',self.partner_id.id)])
            if room_obj.id :
                raise ValidationError(_('Student already have a Tenancy'))

    @api.model
    def create(self, vals):
        tenancy_model = super(StudentTenancy, self).create(vals)
        student_payment_model = self.env['student.payment']
        date_start = vals['checkin']
        date_end = vals['checkout']
        date_start_obj = datetime.datetime.strptime(date_start, '%Y-%m-%d')
        date_end_obj = datetime.datetime.strptime(date_end, '%Y-%m-%d')
        print("date %s", date_start)
        print("date %s", date_end)
        print("datestart month year", date_start_obj.month, date_start_obj.year)
        while date_start_obj <= date_end_obj :
            print("now its" , date_start_obj.month, date_start_obj.year)
            payment_vals = {'partner_id': vals['partner_id'],
                             'tenancy_id': tenancy_model.id,
                             'room_rate': vals['boarding_cost'],
                             'period': date_start_obj.strftime('%Y-%m-%d'),
                             'status': 'unpaid',
                            }
            student_payment_model.create(payment_vals)
            date_start_obj = self.add_months(date_start_obj, 1) 
        return tenancy_model
    
    def add_months(self, sourcedate, months):
        month = sourcedate.month - 1 + months
        year = sourcedate.year + month // 12
        month = month % 12 + 1
        day = min(sourcedate.day, calendar.monthrange(year,month)[1])
        return datetime.datetime(year, month, day)

class StudentInvoice(models.Model):
    _name = 'student.invoice'
    partner_id = fields.Many2one('res.partner', 'Customer Name', ondelete='cascade', index=True, domain=[('student', '=', True)], required=True)
    tenancy_id = fields.Many2one('student.tenancy')
    order_ids = fields.Many2many('student.payment', string="Order Periode")
    payment_type = fields.Selection(
        [('tenancy', 'Tenancy'),
         ('transport', 'Transport'),
         ('meal', 'Meal'),
         ('deposit', 'Deposit'),
         ('return', 'Return Deposit')
        ], string='Payment Type')
    amount  = fields.Float(string="Amount", compute='_compute_amount', store=True, inverse='_set_inv_amount')
    discount  = fields.Float(string="Discount")
    total  = fields.Float(string="Total Payment", compute='_compute_discount', store=True)
    description  = fields.Char(string="Description")
    posting_date  = fields.Date(string="Posting Date", default=time.strftime("%Y-%m-%d 12:00:00"))
    #boarding_type = fields.Selection(string='state', related='tenancy_id.boarding_type')
    payment_method = fields.Selection(
        [('cash', 'Cash'),
         ('transfer', 'Transfer'),
         ('cheque', 'Cheque'),
         ('creditcard', 'Credit Card'),
         ('ibanking', 'I-Banking'),
         ('other', 'Other')
        ], string='Payment Method')
    status = fields.Selection(
        [('paid', 'Paid'),
         ('unpaid', 'Unpaid')
        ], string='Paid',default='unpaid')

    @api.one
    @api.depends('order_ids.room_rate')
    def _compute_amount(self):
        temp_total = sum(line.room_rate for line in self.order_ids)
        self.amount = temp_total
        if self.discount > 0 :
            self.total = self.amount - (self.amount * (self.discount/100))
        else :
            self.total =self.amount
    
    @api.one
    @api.depends('discount')
    def _compute_discount(self):
        if self.amount > 0 :
            if self.discount > 0 :
                self.total = self.amount - (self.amount * (self.discount/100))
            else :
                self.total =self.amount
    
    def _set_inv_amount(self):
        self._compute_discount()

    @api.onchange('tenancy_id')
    def onchange_tenancy_id(self): 
        if self.tenancy_id :
            id_tenancy = self.tenancy_id.id

            if self.payment_type == 'return' : 
                self.amount = self.tenancy_id.deposit_amount
            if self.payment_type == 'meal' or self.payment_type == 'transport' :
                self.amount = 0

            return {'domain': { 
            'order_ids': [('tenancy_id', '=',id_tenancy)]}} 

    @api.model
    def create(self, vals):
        invoice_model = super(StudentInvoice, self).create(vals)
        if self.payment_type == 'tenancy' : 
            for line in self.order_ids :
                payment_vals = {}
                student_payment_model = self.env['student.payment'].browse(line.id)
                #payment_vals['id'] = line.id
                payment_vals['status'] = self.status
                payment_vals['amount'] = self.amount
                payment_vals['discount'] = self.discount
                payment_vals['total'] = self.total
                payment_vals['description'] = self.description
                payment_vals['posting_date'] = self.posting_date
                payment_vals['payment_method'] = self.payment_method
                payment_vals['invoice_id'] = invoice_model.id
                student_payment_model.write(vals=payment_vals)
        return invoice_model
    
    @api.multi
    def write(self, vals):
        invoice_model = super(StudentInvoice, self).write(vals)
        if self.payment_type == 'tenancy' : 
            for line in self.order_ids :
                payment_vals = {}
                student_payment_model = self.env['student.payment'].browse(line.id)
                #payment_vals['id'] = line.id
                payment_vals['status'] = self.status
                payment_vals['amount'] = self.amount
                payment_vals['discount'] = self.discount
                payment_vals['total'] = self.total
                payment_vals['description'] = self.description
                payment_vals['posting_date'] = self.posting_date
                payment_vals['payment_method'] = self.payment_method
                payment_vals['invoice_id'] = self.id
                #print(payment_vals)
                student_payment_model.write(vals=payment_vals)
        return invoice_model

    @api.multi
    def unlink(self):
        if self.order_ids  :
            for line in self.order_ids :
                payment_vals = {}
                student_payment_model = self.env['student.payment'].browse(line.id)
                #payment_vals['id'] = line.id
                payment_vals['status'] = 'unpaid'
                payment_vals['amount'] = 0
                payment_vals['discount'] = 0
                payment_vals['total'] = 0
                payment_vals['description'] = None
                payment_vals['posting_date'] = None
                payment_vals['payment_method'] = None
                payment_vals['invoice_id'] = None
                #print(payment_vals)
                student_payment_model.write(vals=payment_vals)
        super(StudentInvoice, self).unlink()
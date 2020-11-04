from odoo import fields, models, api

class Partner(models.Model):
    _inherit = 'res.partner'
    
    # Add a new column to the res.partner model, by default partners are not
    # instructors
    student = fields.Boolean("Student")
    student_class = fields.Char()
    chinese_name = fields.Char(string="Chinese Name")
    race = fields.Char(string="Race")
    religion = fields.Char(string="Religion")
    gender = fields.Selection(string='Gender',selection=[('male', 'Male'), ('female', 'Female')])
    birthdate = fields.Date()
    identification_number = fields.Char(string="ID Number")
    mobile = fields.Char(string="Handphone Number")
    type = fields.Selection(
        [('contact', 'Contact'),
         #('invoice', 'Invoice address'),
         #('delivery', 'Shipping address'),
         #('other', 'Other address'),
         ("private", "Private Address"),
        ], string='Address Type',
        default='contact',
        help="Used by Sales and Purchase Apps to select the relevant address depending on the context.")
    data_status = fields.Boolean(string='is Active',default=True)
    # CONTACT TYPE 
    contact_type = fields.Selection(string='Contact Type',selection=[('contract', 'Contract'), ('homestayer', 'Home Stayer'), ('shortterm', 'Short Term')])
    group_type = fields.Selection(string='Group',selection=[('aeis', 'AEIS/S-AEIS TEST'), ('bca', 'BCA TEST'), ('studytour', 'Study Tour'), ('tyu', 'tyu')])
    contact_remark = fields.Selection(string='Contact Status Remark',selection=[('complete', 'Complete'), ('incomplete', 'Incomplete')])
    office_phone = fields.Char(string="Office Phone Number")
    # session_ids = fields.Many2many('openacademy.session',
    #     string="Attended Sessions", readonly=True)
    # Parent/Guardian Information
    #guardians_ids = fields.One2many('res.partner.guardian', 'partner_id', string='Guardian Information')  # force "active_test" domain to bypass _search() override
    is_guardian = fields.Boolean(string='is Parent')
    school_ids = fields.One2many('student.student.schools', 'partner_id', string='Education')
    valid_ids = fields.One2many('student.validation', 'partner_id', string='Validation')
    payment_ids = fields.One2many('student.payment', 'partner_id',readonly=True, string='Payment')

    @api.depends('parent_id')
    def _compute_student(self):
        if self.parent_id:
            self.student=False

class PartnerGuardian(models.Model):
    _name = 'res.partner.guardian'
    partner_id = fields.Many2one('res.partner', 'Account Holder', ondelete='cascade', index=True, domain=[('is_company', '=', False)], required=True)
    name = fields.Char(related='partner_id.name', readonly=False)
    type = fields.Selection(related='partner_id.type', readonly=False)


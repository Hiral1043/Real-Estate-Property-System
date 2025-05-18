from odoo import api,models,fields
from tabnanny import check
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression

class RealEstate(models.Model):
    _name = "estate.property"
    _description = "Estate property"
    _rec_name = "title"
    _order = "id desc" 

    image = fields.Image()
    title = fields.Char("Title",required=True)
    descriptiom = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date() 
    expected_price = fields.Float(required=True,default=0.0)
    _sql_constraints = [('must_positive','CHECK(expected_price > 0)','expected price must be postive')]
    selling_price = fields.Float(default=0.0)
    bedrooms = fields.Integer(default="3")
    living_area = fields.Integer(copy=True)
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([('north','north'), 
                                      ('south','south'),
                              ('east','east'),
                              ('west','west')],
                        help = "used for orientation")
    active = fields.Boolean(default=True)
    status = fields.Selection([('new','New'), 
                            ('offer_received','offer_received'),
                            ('offer_accepted','offer accepted'),
                            ('sold','Sold'),
                            ('cancel','Cancel')],
                            default = "new",
                            help = "select the status")
    property_type_id = fields.Many2one(comodel_name="estate.property.type", string="property type")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesperson = fields.Many2one("res.users", string="salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags") 
    offer_ids = fields.One2many("estate.property.offer","property_id",string = "Offers")   
    total_area = fields.Float(compute="_compute_total",store=True)
    invoice_id = fields.Many2one('account.move')
    invoice = fields.Integer(compute="_compute_invoice_count",store=True)

        
    def _compute_invoice_count(self):
        for record in self:
            record.invoice = self.env['account.move'].search_count([
                ('property_id', '=', self.id),
                ('move_type', '=', 'out_invoice') 
            ])

    def action_count_invoices(self):    
        return {   
            "type": "ir.actions.act_window",
            "name": "Customer Invoice",
            "view_mode": "list,form",
            "res_model": "account.move",
            "res_id": self.invoice,
            "domain": [("id", "=", self.invoice)],
            "target": "current"
        }
        
            

    # to add multiple feild name to _rec.name
    combination = fields.Char(compute='_compute_fields_combination')

    @api.depends('title', 'descriptiom')
    def _compute_fields_combination(self):
        for test in self:
            test.combination = test.title + ' ' + test.postcode

    # adding the area of houseusing compute funtion
    @api.depends("living_area","garden_area")
    def _compute_total(self):
        for i in self:
            i.total_area = i.living_area + i.garden_area

    # compute function
    best_offer=fields.Float(compute="_compute_best_price",store=False)
    @api.depends("offer_ids")
    def _compute_best_price(self):
        for i in self:
            i.best_offer = max(i.offer_ids.mapped("price"),default=0.00)
            
    # on change concept implementation
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation ='north'
        else:
            self.garden_area = 0
            self.garden_orientation =False
           
    # action of once the property is sold it cant be canceled    
    def action_sold(self):
        for record in self:
            if record.status == "cancel":
                raise UserError('you can\'t Sold this property')
            else:
                record.status = "sold"
        return True
    # action of once the property is sold it cant be canceled
    def action_cancel(self):
        for record in self:
            if record.status == "sold":
                raise UserError('you can\'t cancel this property')
            else:
                record.status = "cancel"
        return True
    
    @api.constrains('selling_price', 'expected_price')
    def check_selling_price(self):
        for record in self:
            if record.selling_price == 0:
                continue
            if (record.selling_price <  (record.expected_price * 0.9)):
                raise ValidationError("The selling price must be atleast 90 percent of expected price! you must reduce the excepected price if you want to accept this offer ")

    @api.constrains('postcode')
    def check_postcode(self):
        if not (self.postcode.isdigit() and len(self.postcode) == 8):
            raise ValidationError("postcode should be integer and of lenght 8 digits")
        
              
    # this is python constrain for excepted price and selling price
    @api.constrains('expected_price')
    def _check_expected_price(self):
        for record in self:
            if record.expected_price < 0:
                raise ValidationError("expected_price must be postivie")
            
    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price < 0:
                raise ValidationError("selling_price must be postivie")


    # dont allow to delete record when status is new and cancel
    def unlink(self):
        for record in self:
            if record.status in ['new','cancel']:
                raise ValidationError('you can\'t delete this record....')
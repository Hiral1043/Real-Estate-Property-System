from odoo import api,models,fields
from dateutil.relativedelta import relativedelta
from datetime import date, timedelta
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression
from odoo.tools import float_compare

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _order = "price desc"
    _description = "Estate property Offer"


    property_id = fields.Many2one("estate.property",required=True)
    price = fields.Float()
    status = fields.Selection([("accept","Accepted"),
                                ("reject","Rejected")],copy=False) #when copy is false it dont allow to copy data when record is duplicated
    partner_id = fields.Many2one("res.partner",required=True)
    validity=fields.Integer(default=7)
    date_deadline=fields.Datetime(compute="_compute_date_deadline",inverse="_inverse_date_deadline")  #it is implementation of inverse funcion 
    description = fields.Char(related="partner_id.name")
    # related feilds 
    property_type_id=fields.Many2one(related="property_id.property_type_id",store=True) 
    
    @api.depends("validity")
    def _compute_date_deadline(self):
        for i in self:
            i.date_deadline = False
            if i.create_date:
                i.date_deadline = (i.create_date.date() + relativedelta(days=i.validity))
    
    def _inverse_date_deadline(self):
        for i in self:
            if i.date_deadline:
                i.validity = (i.date_deadline.date() - i.create_date.date()).days


    def action_status_accept(self):
        for record in self:
            if 'accept' in record.mapped("property_id.offer_ids.status"):
                raise UserError("the offer already acccepted....")
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.status ="accept"
            record.property_id.status = "offer_accepted"
        
        

    def action_status_reject(self):
        for record in self:
            if record.status == "accept":
                raise UserError("The offer is already selected")
            record.status ="reject"
            record.property_id.selling_price=False
            record.property_id.buyer_id = False
          
    
    @api.constrains('price')
    def _check_price(self):
        for record in self:
            if record.price < 0:
                raise ValidationError("price must be postivie")
            
    @api.model
    def create(self, vals_list):
        if vals_list.get("property_id") and vals_list.get("price"):
            property = self.env["estate.property"].browse(vals_list["property_id"])
            # We check if the offer is higher than the existing offers
            if property.offer_ids:
                max_offer = max(property.mapped("offer_ids.price"))
                if vals_list["price"] < max_offer:
                # if float_compare(vals["price"], max_offer, precision_rounding=0.01) <= 0:
                    raise UserError("The offer must be higher than %.2f" % max_offer)
            property.status = "offer_received"
            print("\n\n\n\n\n\n>>>>>>>vals_list",vals_list)
        return super().create(vals_list)
    

           
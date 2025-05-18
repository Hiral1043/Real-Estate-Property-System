import re
from odoo import api,models
from odoo.exceptions import UserError, ValidationError


class Partner(models.Model):
    _inherit = "res.partner"


    @api.constrains('phone')
    def validate_phone(self):
        for record in self:
            if not (record.phone.isdigit() and len(record.phone) == 10):
                raise UserError('phone number must be of 10 digit and numeric') 
        

    @api.onchange('email')
    def validate_mail(self):
        for record in self:    
            if record.email:
                match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', record.email)
                if match == None:
                    raise ValidationError('Not a valid E-mail ID')
                
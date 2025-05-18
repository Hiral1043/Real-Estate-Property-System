from odoo import api,models,fields

class SoldPropertyWizard(models.TransientModel):
    _name = "sold.property.wizard"
    _description = "Sold Property Wizard"

    name = fields.Char()
    def sold_property_wizard(self):
        print("heellllo")

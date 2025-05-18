from odoo import models,Command, fields

class Estate(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        journal = self.env["account.journal"].search([('type','=','sale')], limit=1)
   
        account = self.env["account.move"].create(
            {
                'journal_id':journal.id,
                'move_type':'out_invoice',
                'partner_id':self.buyer_id.id,
                'property_id':self.id,
                "invoice_line_ids": [
                    Command.create({
                        "name" : self.title,
                        "quantity": 1,
                        "price_unit" : self.selling_price
                    }),
                    Command.create({
                        "name" : f"6% of the selling price",
                        "quantity": 1,
                        "price_unit" :self.selling_price * 0.06
                    }),
                    Command.create({
                        "name" : "Administrative fees",
                        "quantity": 1,
                        "price_unit" :100
                    })
                ],
            }
        )
        
        print("\n\n\n===========account", account)
        return super().action_sold()
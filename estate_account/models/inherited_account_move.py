from odoo import fields,models,api

class InheritedAccountMove(models.Model):
    _inherit = "account.move"

    property_id = fields.Many2one("estate.property")

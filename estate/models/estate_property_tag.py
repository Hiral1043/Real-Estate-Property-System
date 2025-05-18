from odoo import models,fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _order = "name"
    _description = "Estate property tag"

    name = fields.Char("Name",required=True)
    _sql_constraints=[
    (
        'tag_unique',
        'UNIQUE(name)',
        'the tag must be unique'
    )]
    color=fields.Integer()
    
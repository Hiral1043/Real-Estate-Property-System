# from enum import UNIQUE
from odoo import api,models,fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _order = "name"
    _order = "sequence"
    _description = "Estate property type"
    

    name = fields.Char("name",required=True)
    _sql_constraints=[
    (
        'unique_name_type',
        'UNIQUE(name)',
        'the type must be unique'
    )
    ]
    property_ids = fields.One2many("estate.property","property_type_id")
    sequence = fields.Integer('Sequence')
    offer_ids=fields.One2many('estate.property.offer','property_type_id')
    offer_count=fields.Integer(compute="_compute_offer_count")
    property_type_count = fields.Integer(compute="_compute_property_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)


    @api.depends("property_type_count")
    def _compute_property_count(self):
        for record in self:
            record.property_type_count = len(record.property_ids)


    def action_offers(self):
        return{
            'type' : 'ir.actions.act_window',
            'view_mode' : 'list',
            'name' : 'action_offers',
            'res_model' :'estate.property.offer',
            'view_id': self.env.ref('estate.estate_property_offer_view_list').id,
            'domain': [('property_type_id','=', self.id)]
            }
    def action_property_count(self):
        return{
            'type' : 'ir.actions.act_window',
            'view_mode' : 'list',
            'name' : 'action_property_count',
            'res_model' :'estate.property',
            'view_id': self.env.ref('estate.estate_property_view_list').id,
            'domain': [('property_type_id','=', self.id)]
            }
                

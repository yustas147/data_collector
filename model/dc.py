# -*- coding: utf-8 -*-
from openerp import models, fields, api
import logging

_logger = logging.getLogger(__name__)

    
class dc_page(models.Model):
     
    _name = 'dc.page'
    _rec_name = 'base_url'
    
    def get_full_url(self, *args, **kwargs):
        ''' Returns full page address adding some keyword
        value (fex 'suffix=xxxxx' to base_url'''
        
        suffix = kwargs.get('suffix','')
        res = self.base_url
        if suffix:
            res = '/'.join([self.base_url,suffix])
        return res
    
    base_url = fields.Char(string="Base URL")
    el_ids = fields.One2many(comodel_name='dc.el', inverse_name='page_id', 
                            string='Elements')
    

    
class dc_el(models.Model):
    ''' Element of web page '''
    _name = 'dc.el'
    
    name = fields.Char(string="Data field name")
    page_id = fields.Many2one(comodel_name="dc.page", string="Page Containing")
    x_path = fields.Char(string="Xpath on the page") 
    model_id = fields.Many2one(comodel_name='ir.model', string='Model')
    attr_ids = fields.Many2many(comodel_name='dc.attr', relation='el_attr_rel', string='Attributes')
    property_id = fields.Many2one(comodel_name='dc.property', string='Property')

class dc_attr(models.Model):
    ''' Attribute name '''
    _name = 'dc.attr'
    
    name = fields.Char(string="Attribute")
    el_ids = fields.Many2many(comodel_name='dc.el', relation='el_attr_rel', string='Elements')
    
    
class dc_property(models.Model):
    _name = 'dc.property'
    
    name = fields.Char(string='Property')
    el_ids = fields.One2many(comodel_name='dc.el', inverse_name='property_id', 
                            string='Elements')
        

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
    
    @api.multi
    def get_full_page(self, act_id = False):
        for slf in self:
            res = slf.page_id.base_url
            suff = slf.page_suffix_id.get_suffix(act_id = act_id)
            if suff:
                res += '/' + suff
            _logger.info('get_full_page result is: ------------------------------------------------- %s' % (unicode(res)))
            return res
        
    @api.multi
    def get_name_value(self, val):
        for i in self:
            try:
                exec(i.name_trans)
                return calcu(val)
            except:
                pass
    
    name = fields.Char(string="Data field name")
    page_id = fields.Many2one(comodel_name="dc.page", string="Page Containing")
    page_suffix_id = fields.Many2one(comodel_name="dc.page_suffix", string="Page Suffix")
    #page_full = fields.Char(string='Full Page URL', compute='get_full_page')
    x_path = fields.Char(string="Xpath on the page") 
    model_id = fields.Many2one(comodel_name='ir.model', string='Model')
    attr_ids = fields.Many2many(comodel_name='dc.attr', relation='el_attr_rel', string='Attributes')
    property_id = fields.Many2one(comodel_name='dc.property', string='Property')
    name_trans = fields.Text(string="Function to bring the value of name")
    
    

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

class dc_page_suffix(models.Model):
    _name = 'dc.page_suffix'
        
    @api.onchange('model_id')
    def _gmid(self):
        res = {'domain':''} 
        vlst = self.model_id.field_id.mapped('id')
        res['domain'] = {'fld': [('id', 'in', vlst)]}
        _logger.info('gmid run!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1!')
        return res
    
    def get_suffix(self, act_id = False):
        res = ''
        if self.name:
            res = self.name
#            return dict(str_value = self.name)
            return res
        else:
            if self.fld:
                if act_id:
                    env = self.env[self.model_id.model]
                    res = getattr(env.browse(act_id), self.fld.name)
#                return dict(field_name = self.fld.name)
                    return res
        _logger.info('get_suffix Returned empty suffix!!!!!!')
        return res
            
    name = fields.Char(string='Suffix')
    model_id = fields.Many2one(comodel_name='ir.model', string='Model ID')
    fld = fields.Many2one(comodel_name='ir.model.fields', string='Field')
    
            
        
        

# -*- coding: utf-8 -*-
from openerp import models, fields, api
import logging
from  ..unit import base_parser, bin_fetcher
from time import sleep
from os import name as osname
_logger = logging.getLogger(__name__)

class res_partner(models.Model):
    _inherit='res.partner'    
    
    _order = 'last_month_sales desc'
    @api.multi
    def get_dc_elements(self):
        ''' Searches in db for elements to fetch from web pages
        for current models record.
        Returns dict with dc.page`s as keys and list`s of dc.el`s as a values'''
        env = self.env
        for i in self:
            els = env['dc.el'].search([('model_id.model', '=', i._name)])            
            return els
            
    @api.multi
    def process_element(self, el, url=None):
        for i in self:
            res = dict(url=url, x_path=el.x_path, fname=el.name, attr=el.attr_ids.mapped('name'))
#            res = dict(url=el.page_id.base_url, x_path=el.x_path, fname=el.name, attr=el.attr_ids.mapped('name'))
            if el.property_id:
                res.update({'property': el.property_id.name})
            return res
#            return dict(url=el.page_id.base_url, x_path=el.x_path, fname=el.name, attr=el.attr_ids.mapped('name')[0])
#            return dict(url=el.page_id.base_url, x_path=el.x_path, fname=el.name, attrs=el.attr_ids.mapped('name'))
    
    @api.multi
    def get_page_full_url(self, page, suffix=False):
        ''' Model-sided suffix adding''' 
        if not suffix:
            suffix = self.plk
#            suffix = self.plk
            
        for i in self:
            return '/'.join([page,suffix])
    
    @api.multi
    def render_page(self, url, suffix=None):
        parser = base_parser.phantomjs_parser()
        #furl = self.get_page_full_url(url, suffix=suffix)
        furl = url
        page = parser.set_page(furl)
        return page
        
    @api.multi
    def parse_page(self, page, **kwargs):
        x_path = kwargs.get('x_path')
        try:
            res = page.find_element_by_xpath(x_path)
            
            if res:
                prop = kwargs.get('property')
                attr = kwargs.get('attr')
                if prop:
                    res = res.get_property(prop)
                else:
                    if len(attr):
                        res = res.get_attribute(attr[0])
                    
            _logger.info('parse res is %s' % unicode(res))
            return res        

        except:
            _logger.info('Not found element %s' % unicode(x_path))
    
    
    @api.multi
    def parse(self, **kwargs):
        parser = base_parser.phantomjs_parser()
        url = kwargs.get('url')
        url = self.get_page_full_url(url)
        page = parser.set_page(url)
        x_path = kwargs.get('x_path')
        res = page.find_element_by_xpath(x_path)
        #if len(res) > 0:
            #if len(res) > 1:
                #_logger.info('res len is more than 1 : %s' % unicode(len(res)))
        prop = kwargs.get('property')
        attr = kwargs.get('attr')
        if prop:
#        if len(attr):
#        if attr:
            res = res.get_property(prop)
#            res = res.get_property(attr[0])
#            res = res.get_property(attr)
        else:
            if len(attr):
                res = res.get_attribute(attr[0])
                
        _logger.info('parse res is %s' % unicode(res))
        try:
            xxx = parser.driver.quit()
        except:
            _logger.info('Phantom was not killed successfully, xxx: %s', (unicode(xxx)))
            
            pass
        return res
            
                        
    @api.multi
    def get_my_data(self):
        for i in self:
            res = {}
            elems = i.get_dc_elements()
#            elems = self.get_dc_elements()
            _logger.info('elems: %s' % unicode(elems))
            #urls = elems.mapped('page_id')]
            ''' getting full urls '''
            urls = [ el.get_full_page(act_id=i.id) for el in elems ]
            #lets make urls unique
            urls = set(urls)
            
            for u in urls:
                i.page = i.render_page(u)
                page = i.page
#                page = i.render_page(u)
                for el in elems:
         #           if el.page_id == u:
                    if el.get_full_page(act_id=i.id) == u:
                        parse_args = i.process_element(el, url=u)
                        resi = i.parse_page(page, **parse_args)
                        if el.name_trans:
                            resi = el.get_name_value(resi)
                        res.update(dict([(el.name, resi)]))
            #try:
                #page.driver.quit()
            #except:
                #_logger.info('phantom driver quit trouble')
                #pass                        
                
            _logger.info('res is %s' % unicode(res))
            return res, page
#            return res
        
    @api.multi
    def update_my_data(self):
        for i in self:
            fdata, page = i.get_my_data()
#            fdata = i.get_my_data()
            try:
                if i.partner_license_key:
                    i.i502 = 'https://502data.com/license/'+unicode(i.partner_license_key)
            except:
                pass
            i.write(fdata)
            st = 2
            _logger.info('sleep for %s sec' % unicode(st))
            sleep(st)
            try:
                if osname == 'nt':
                    page.quit()
            except:
                pass
    
        
        

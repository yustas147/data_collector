# -*- coding: utf-8 -*-
from openerp import models, fields, api
import logging
from  ..unit import base_parser, bin_fetcher
_logger = logging.getLogger(__name__)

class res_partner(models.Model):
    _inherit='res.partner'    
    
    @api.multi
    def get_dc_elements(self):
        ''' Searches in db for elements to fetch from web pages
        for current models record.
        Returns dict with dc.page`s as keys and list`s of dc.el`s as a values'''
        env = self.env
        for i in self:
            els = env['dc.el'].search([('model_id.model', '=', i._name)])            
            return els
            #for el in els:
                #k = el.page_id.id
                #v = unicode(el)
                #if not res.get(k, ''):
                    #res.update({k : []})
                #res[k].append(v)
            #_logger.info('get_dc_elements res: %s' % unicode(res))            
            #for k in res:
                
                #_logger.info('eval key: %s' % eval(res[k]).base_url)            
            #return res
            
    @api.multi
    def process_element(self, el):
        for i in self:
            res = dict(url=el.page_id.base_url, x_path=el.x_path, fname=el.name, attr=el.attr_ids.mapped('name'))
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
            
        for i in self:
            return '/'.join([page,suffix])
    
    @api.multi
    def render_page(self, url):
        parser = base_parser.phantomjs_parser()
        furl = self.get_page_full_url(url)
        page = parser.set_page(furl)
        return page
        
    @api.multi
    def parse_page(self, page, **kwargs):
        #parser = base_parser.phantomjs_parser()
        #url = kwargs.get('url')
        #url = self.get_page_full_url(url)
        #page = parser.set_page(url)
        x_path = kwargs.get('x_path')
        res = page.find_element_by_xpath(x_path)
        prop = kwargs.get('property')
        attr = kwargs.get('attr')
        if prop:
            res = res.get_property(prop)
        else:
            if len(attr):
                res = res.get_attribute(attr[0])
                
        _logger.info('parse res is %s' % unicode(res))
        #try:
            #parser.driver.quit()
        #except:
            #pass
        return res        
    
    
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
            parser.driver.quit()
        except:
            pass
        return res
            
                        
    @api.multi
    def get_my_data(self):
        for i in self:
            res = {}
            elems = self.get_dc_elements()
            _logger.info('elems: %s' % unicode(elems))
            urls = elems.mapped('page_id')
            for u in urls:
                page = i.render_page(u.base_url)
                for el in elems:
                    if el.page_id == u:
                        parse_args = i.process_element(el)
                        resi = i.parse_page(page, **parse_args)
                        res.update(dict([(el.name, resi)]))
                        
            #for el in elems:
                #parse_args = i.process_element(el)
 # #                parse_args = self.process_element(el)
                #resi = i.parse(**parse_args)
# #                resi = self.parse(**parse_args)
                #res.update(dict([(el.name, resi)]))
                
            _logger.info('res is %s' % unicode(res))
            return res
        
    @api.multi
    def update_my_data(self):
        for i in self:
            fdata = i.get_my_data()
            i.write(fdata)
    
        
        
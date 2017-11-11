# -*- coding: utf-8 -*-

import requests
from  lxml import html, etree
import logging
from selenium import webdriver
import os

_logger = logging.getLogger(__name__)

class base_parser(object):
    def __init__(self, url):
        self.url = url        
    
    def take_from_url(self):
        if self.url:
            res = requests.get(self.url, allow_redirects=True, verify=False).text
            self.page_text = res
            return(self.page_text)
    
    def get_html_tree(self, text=None):
        if not text:
            if not self.page_text:
                text = self.take_from_url()
            else:
                text = self.page_text
                
        self.html_tree = html.fromstring(text)
        return self.html_tree
    
    def get_block_unparsed_lines(self, html_tree=None, block_pattern=None):
        '''Return block of unparsed lines from lxml tree (source_tree) using xpath pattern block_pattern'''
        
        if not block_pattern:
            return False
        
        if not html_tree:
            if not self.html_tree:
                html_tree = self.get_html_tree()
            else:
                html_tree = self.html_tree
                
        _logger.info('get_block_unparsed_lines returns  : %s'  % unicode(html_tree))
        result = html_tree.xpath(block_pattern)
        _logger.info('get_block_unparsed_lines result  : %s'  % unicode(result))
        _logger.info('len(result)  : %s'  % unicode(len(result)))
        
        try:
            result = result[0]
        except IndexError:
            _logger.info('Index Error !!!!!!!!!!!!!!!!!!! ')
            return False
        
        self.block_unparsed_lines = result
        return self.block_unparsed_lines
    
    def get_unparsed_lines(self, pattern=None):
        
        _logger.info('gul pattern is : %s'  % unicode(pattern))
        try:
            gbul = self.block_unparsed_lines
        except AttributeError:
            return False
            
#        gbul = self.get_block_unparsed_lines(self.block_unparsed_lines, pattern)
        _logger.info('gbul : %s'  % unicode(gbul))
        if gbul:
            res = self.block_unparsed_lines.xpath(pattern)
#            res = self.block_unparsed_lines.xpath(pattern)
            _logger.info('get_unparsed_lines returns  : %s'  % unicode(res))
            return res
        else:
            pass
            #_logger.info('get_unparsed_lines returns  : %s'  % unicode(unparsed_lines))
        return False
    
    def get_record_uline_patt(uline, patt):
        ''' Get record from unparsed line uline using pattern patt'''
        result = uline.xpath(patt)[0] 
        return result
    
    def get_phantomjs_driver(self):
        if os.name == 'nt':
            driver = webdriver.PhantomJS(executable_path="c:\\Python27\\phantomjs.exe", port=7777, service_log_path=os.path.devnull)
        else:
            _logger.info('os.path.devnull is %s' % unicode(os.path.devnull))
            driver = webdriver.PhantomJS(executable_path="/usr/bin/phantomjs", port=7777, service_log_path=os.path.devnull)        
        return driver

    def get_image(self, patt):
        #if not self.html_tree:
            #html_tree = self.get_html_tree()
        #else:
            #html_tree = self.html_tree        
        html_tree = self.get_html_tree()        
        #image_link = html_tree.xpath(patt)[0]
        
        if os.name == 'nt':
            driver = webdriver.PhantomJS(executable_path="c:\\Python27\\phantomjs.exe", port=7777, service_log_path=os.path.devnull)
        else:
            _logger.info('os.path.devnull is %s' % unicode(os.path.devnull))
            driver = webdriver.PhantomJS(executable_path="/usr/bin/phantomjs", port=7777, service_log_path=os.path.devnull)
        driver.get(self.url)
        results = driver.find_elements_by_xpath('.//div[@class="col-md-8"]/div[@class="pull-left"]/a/img')
        ires = results[0]
        image_link = ires.get_attribute('src')
        kushguide_href = ires.get_attribute('href')
        if kushguide_href  and signup not in kushguide_href:
            self.kushguide_link = kushguide_href
            _logger.info('kushguide_href is %s' % unicode(self.kushguide_link))
        #driver.quit()
        
        return image_link

    
class basic_parser(object):
    
    def get_phantomjs_driver(self):
        if os.name == 'nt':
            driver = webdriver.PhantomJS(executable_path="c:\\Python27\\phantomjs.exe", port=7777, service_log_path=os.path.devnull)
        else:
            _logger.info('os.path.devnull is %s' % unicode(os.path.devnull))
            driver = webdriver.PhantomJS(executable_path="/usr/bin/phantomjs", port=7777, service_log_path=os.path.devnull)        
        return driver    
    
    def set_phantomjs_driver(self):
        self.driver = self.get_phantomjs_driver()
        return self.driver
    
    
    
class phantomjs_parser(basic_parser):
    
    def __init__(self):
        self.set_phantomjs_driver()
    
    def get_page(self, url):
        self.driver.get(url)
        res = self.driver
        _logger.info('get_page res: %s' % unicode(res))
        return res
    
    def set_page(self, url):
        self.page = self.get_page(url)
        return self.page
    
    def get_el_by_xpath_ind_attr(self, url=False, x_path=False, el_ind=0, attr_name=False):
        if not x_path and attr_name:
            _logger.error("get_el_by_xpath: no x_path or attr_name argument !!!!")
            return False
        if not url:
            if not self.page:
                return False
            else:
                page = self.page
        else:
            page = self.set_page(url)
            
        res = page.find_elements_by_xpath(x_path)[el_ind].get_attribute(attr_name)
        
        return res
        
        
            
        
    
    
    
    
class i502_sales_lm_total(base_parser):

    def get_result(self):
        s = self
        s.take_from_url()            
        s.get_html_tree()            
        s.get_block_unparsed_lines(block_pattern='//table[@class="table table-bordered table-striped"]')            
        unparsed_lines =  s.get_unparsed_lines(pattern='.//tr')        
#        unparsed_lines =  s.get_unparsed_lines(s.block_unparsed_lines, pattern='.//tr')        
        _logger.info('get_result unparsed_lines  : %s'  % unicode(unparsed_lines))
        if unparsed_lines:
            lm_sales, total, image = unparsed_lines[1][1].text, unparsed_lines[-1][1].text, self.get_image(
                './/div[@class="col-md-8"]/div[@class="pull-left"]/a/img/@src') 
            return lm_sales, total, image        
        return False
            
class kushguide_parser(i502_sales_lm_total):
    
    def get_website(self, kushguide_link=False):
        if kushguide_link:
            self.kushguide_link = kushguide_link
        if self.kushguide_link:
            driver = self.get_phantomjs_driver()
            driver.get(self.kushguide_link)
            self.website = driver.find_elements_by_xpath('.//li/a[@data-ng-show="store.website"]/')[0].get_attribute('href')
            if self.website:
                return(self.website)
            
        
    
    

if __name__=='__main__':
    myparser = base_parser('https://502data.com/license/415645')    
    myparser.take_from_url()
    myparser.get_html_tree()
    myparser.get_block_unparsed_lines(block_pattern='//table[@class="table table-bordered table-striped"]')
    unparsed_lines =  myparser.get_unparsed_lines(pattern='.//tr')
    print('Last month sales are %s' % unicode(unparsed_lines[1][1].text))
    print('Total sales are %s' % unicode(unparsed_lines[-1][1].text))
    for node in unparsed_lines:
    #for node in myparser.take_from_url().get_html_tree().get_block_unparsed_lines(pattern='//table[@class="table table-bordered table-striped"]').get_unparsed_lines(pattern='.//tr'):
        l = node.xpath('.//td')
#        l = etree.tostring(node.xpath('.//td'))
        if len(l):
            print len(l)
            for item in l:
                print('etree.tostring(item): %s' % unicode(etree.tostring(item)))
                print(item.text)                



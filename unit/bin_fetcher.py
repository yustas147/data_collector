# -*- coding: utf-8 -*-

#import requests
import urllib2
#from  lxml import html, etree
import logging
#from openerp import http
import base64
from os import name as os_name

class b_fetcher():
    
    def set_url(self, url):
        self.url = url        
        
    def __init__(self, url):
        self.set_url(url)
        if os_name == 'nt':
            self.local_fs_path = './%s' % self.get_file_name_from_url()
        else:
            self.local_fs_path = '/opt/odoo/%s' % self.get_file_name_from_url()
    
    def fetch(self):
        bfile = urllib2.urlopen(self.url)
        with open(self.local_fs_path, mode='wb') as f:
            f.write(bfile.read())
    
    def fetch_to(self, filepath=None):
        if not filepath:
            return self.fetch()
        bfile = urllib2.urlopen(self.url)
        with open(filepath, mode='wb') as f:
            f.write(bfile.read())
            
    def get_file_name_from_url(self):
        return unicode(self.url.split('/')[-1])
    
    def get_odoo_path(self):
        addons_path = http.addons_manifest['web']['addons_path']
        print unicode(addons_path)
            
if __name__=='__main__':
    
    
    fetcher = b_fetcher('https://res.cloudinary.com/the-kush-guide/image/upload/v1468527706/nrc1k9u8edetvbggblev.jpg')
    fetcher.get_odoo_path()
    #fetcher.fetch()
    #fetcher = b_fetcher('http://www.mainstmj.com/wp-content/uploads/2016/07/LogoMSM.png')
    #fetcher.fetch()
                
    
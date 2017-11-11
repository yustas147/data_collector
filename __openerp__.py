# -*- coding: utf-8 -*-
{
    'name': "Helper models for web data collector",
    'author': "Simbioz, Yury Stasovsky",
    'license': 'LGPL-3',
    'website' : "https://qarea.us",
    'category': 'Custom integration',
    'version': '1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],
#    'depends': ['sale', 'purchase', 'mrp', 'sce'],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        #'security/groups.xml',
       # 'wizard/wiz_view.xml',
        'views/models.xml',
        'views/menu.xml',
        'views/res_partner.xml',
    ],
    'installable': True,
}

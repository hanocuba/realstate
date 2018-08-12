# -*- coding: utf-8 -*-
{
    'name': "map_leaft",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Odoo  widgets',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['web', 'base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/left_map_assets.xml',
    ],
    'qweb': [
        'static/src/xml/resource.xml'
    ],
    # only loaded in demonstration mode
    'demo': [

    ],
    'installable': True,
    'application': False,
    'bootstrap': True,
    'auto_install': False,
}
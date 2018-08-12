# -*- coding: utf-8 -*-
{
    'name': "realstate_rent_room",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Módulo Desarrollado por Luis Felipe Domínguez Vega, Dairon Domínguez Vega, bajo supervisión de Hanoi Calvo Fernandez, para la empresa Real State platform... para la plataforma de gestion de rentas, ventas de casas y alquileres de locales para eventos de dicha empresa...
    """,

    'author': "LDH",
    'website': "scnetisla@gmail.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'product',
        'map_leaft',
        'contract'
    ],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',

        'views/rent_place_views.xml',
        'views/rent_place_image_views.xml',
        'views/contract_recurring_form_view_inherit.xml',


        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
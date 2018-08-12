# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools
from odoo.exceptions import ValidationError
from odoo.modules import get_module_resource
from odoo.tools.translate import _


class RentPlace(models.Model):
    _name = "realstate_rent_room.rent_place"

    def _default_image(self):
        image_path = get_module_resource('hr', 'static/src/img', 'default_image.png')
        return tools.image_resize_image_big(open(image_path, 'rb').read().encode('base64'))

    name = fields.Char(
        string="Nombre"
    )
    description = fields.Text(
        string=u"Descripción"
    )
    for_sale = fields.Boolean(string='En venta')
    state = fields.Selection(selection=[('rented', 'Rentada'), ('free', 'Libre')],
                             string='Estado', default='free')
    active = fields.Boolean(string='Archivar', default=True)
    likes_id = fields.Many2many(
        comodel_name='realstate_rent_room.rent_place_like',
        relation='rent_place_rent_place_like_m2m',
        column1='rent_place_id',
        column2='rent_place_like_id'
    )
    place_number = fields.Char(
        string="Identificador del local"
    )
    list_services_id = fields.One2many(
        comodel_name="product.product",
        inverse_name="place_id",
        string="Servicios asociados"
    )
    place_type_id = fields.Many2one(
        comodel_name="realstate_rent_room.rent_place_type",
        string='Tipo'
    )
    extra_info_id = fields.One2many(
        comodel_name="realstate_rent_room.rent_place_info",
        inverse_name="rent_place_id",
        string=u"Información extra"
    )
    parent_id = fields.Many2one(
        comodel_name="realstate_rent_room.rent_place",
        string='Padre'
    )
    children_id = fields.One2many(
        comodel_name="realstate_rent_room.rent_place",
        inverse_name="parent_id",
        string="Sublocales"
    )

    images_id = fields.One2many(comodel_name='realstate_rent_room.rent_place_image',
                               inverse_name='rent_place_id',
                               string='Fotos')
    image_gallery = fields.Char(compute='compute_images_lst', string=u'Galería')

    # image: all image fields are base64 encoded and PIL-supported
    image = fields.Binary(string="Foto", default=_default_image, attachment=True,
                          help="This field holds the image used as photo for the factory, limited to 1024x1024px.")
    image_medium = fields.Binary("Medium-sized photo", attachment=True,
                                 help="Medium-sized photo of the factory. It is automatically "
                                      "resized as a 128x128px image, with aspect ratio preserved. "
                                      "Use this field in form views or some kanban views.")
    image_small = fields.Binary("Small-sized photo", attachment=True,
                                help="Small-sized photo of the factory. It is automatically "
                                     "resized as a 64x64px image, with aspect ratio preserved. "
                                     "Use this field anywhere a small image is required.")
    contracts_id = fields.One2many(comodel_name='account.analytic.account',
                                   inverse_name='rent_place_id', string='Contratos')

    @api.depends('images_id')
    def compute_images_lst(self):
        # TODO: Update using s.image_id.ids
        for s in self:
            values = ""
            for img in s.images_id:
                values += str(img.id) + ","

            if values:
                values = values[:-1]

            s.image_gallery = values

    @api.multi
    def create_contract(self):

        lines = []

        service_queue = []

        service_queue.append(self)
        # 'reference': self.code,
        # 'type': 'out_invoice',
        # 'partner_id': self.partner_id.address_get(
        #     ['invoice'])['invoice'],
        # 'currency_id': currency.id,
        # 'journal_id': journal.id,
        # 'date_invoice': self.recurring_next_date,
        # 'origin': self.name,
        # 'company_id': self.company_id.id,
        # 'contract_id': self.id,
        # 'user_id': self.partner_id.user_id.id,
        while len(service_queue):
            current = service_queue.pop()

            if current.children_id:
                service_queue.append(self.env['realstate_rent_room.rent_place'].search([('id', 'in', current.children_id.ids)]))

            for l in current.list_services_id:
                lines.append([0, 0, {
                    'product_id': l.id,
                    'quantity': 1,
                    'specific_price': l.lst_price,
                    'uom_id': l.uom_id.id,
                    'name': 'Renta de local',
                    'automatic_price': False
                }])

        return {
            'name': 'Nuevo Contrato',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.analytic.account',
            # 'view_id': self.env.ref('realstate_rent_room.contract_account_inherit_form').id,
            'view_id': self.env.ref('contract.account_analytic_account_recurring_form_form').id,
            'type': 'ir.actions.act_window',
            # 'res_id': self.id,
            'target': 'current',
            'context': {
                'default_name': 'Alquiler / %s' % self.name,
                'default_recurring_invoice_line_ids': lines,
                'default_is_contract': True,
                'search_default_not_finished': True,
                'search_default_recurring_invoices': True,
                'default_recurrent_invoices': True
            }
        }

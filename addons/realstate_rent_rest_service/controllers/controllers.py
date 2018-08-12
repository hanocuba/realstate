# -*- coding: utf-8 -*-

from odoo.http import Controller, request, route
from ..extra.http import make_response


class RestApi(Controller):
    @route('/api/auth', auth='public', methods=["POST"], csrf=False)
    @make_response()
    def authenticate(self, db, login, password):
        # Before calling /api/auth, call /web?db=*** otherwise web service is not found
        request.session.authenticate(db, login, password)
        return request.env['ir.http'].session_info()

    @route('/api/v1/user/create', auth='public', type='json', methods=['POST'], csrf=False)
    def api_create_user(self, **kwargs):
        data = kwargs['kwargs']

        try:
            request.env['res.users'].create({
                'login': data['email'],
                'new_password': data['password'],
                'name': data['name'] + ' ' + data['last_name'],
                'costumer': True
            })

        except:  # Don't catch any base Exception
            return {"data": {'created': False}, "err": 'Usuario existente'}

        return {"data": {'created': True}, "err": False}

    @route('/api/v1/place/suggestions', auth='user', type='json', methods=['POST'], csrf=False)
    def api_suggestions(self, **kwargs):

        search = kwargs['kwargs']["search"]

        results = []

        for elem in request.env['realstate_rent_room.rent_place'].search([('name', 'ilike', '%'+str(search)+'%')]):
            services = []
            for service in elem.list_services_id:
                services.append({
                    'name': service.name
                })

            extra_infos = []
            for extra_info in elem.extra_info_id:
                extra_infos.append({
                    'key': extra_info.name,
                    'value': extra_info.value
                })

            children = []
            for child in elem.children_id:
                children.append({
                    'name': child.name,
                    'description': child.description
                })

            images = []
            for image in elem.images_id:
                images.append({
                    'name': image.name,
                    'description': image.description,
                    'base64': image.image
                })

            results.append({
                'name': elem.name,
                'description': elem.description,
                'type': elem.place_type_id.name,
                'image': elem.image,
                'place_id': elem.place_number,
                'for_sale': elem.for_sale,
                'state': elem.state,
                'up_likes': elem.likes_id.search_count([('like', '=', True)]),
                'down_likes': elem.likes_id.search_count([('like', '=', False)]),
                'services': services,
                'extra_info': extra_infos,
                'children': children,
                'images': images
            })

        return {"data": results, "err": False}

    @route('/api/v1/user/forgot_password', auth='public', type='json', methods=['POST'], csrf=False)
    def api_user_forgot_password(self, **kwargs):
        data = kwargs['kwargs']

        #try:
            #mail = data['email']
        #except:
        #    return {"data": {'created': False}, "err": 'Usuario existente'}

        return {"data": {'send': True}, "err": False}

    @route('/api/v1/user/validate_email', auth='public', type='json', methods=['POST'], csrf=False)
    def api_user_validate_email(self, **kwargs):
        data = kwargs['kwargs']

        mail = data['email']

        users = request.env['res.users'].search([('login', '=', mail)], limit=1)

        if len(users) > 0:
            user = users[0]
            return {"data": {
                'valid': True,
                'img': user.image,
                'name': user.name,
                'email': user.email
            }, "err": False}
        else:
            return {"data": {'valid': False}, "err": False}

    @route('/api/v1/place/filter_keys', auth='user', type='json', method=['POST'], csrf=False)
    def api_place_filter_keys(self, **kwargs):
        data = []
        for key in request.env['realstate_rent_room.rent_place_info_key'].search([]):
            data.append(key.name)

        return {"data": data, "err": False}

    @route('/api/v1/place/like', auth='user', type='json', method=['POST'], csrf=False)
    def api_place_like(self, **kwargs):
        data = kwargs['kwargs']

        place_id = data['place_id']
        like = data['like']

        like_model = request.env['realstate_rent_room.rent_place_like']

        place_like = like_model.search([('user_id', '=', request.env.user.id), ('place_id', '=', place_id)], limit=1)

        if len(place_like) > 0:
            place_like.like = like
        else:
            like_model.create({
                'user_id': request.env.user.id,
                'place_id': place_id,
                'like': like
            })

        return {"data": {'like': True}, "err": False}

    @route('/api/v1/place/rent', auth='user', type='json', method=['POST'], csrf=False)
    def api_place_rent(self, **kwargs):
        data = kwargs['kwargs']

        start_date = data['start_date']
        end_date = data['end_date']
        service_id = data['service_id']

        rent_place_model = request.env['realstate_rent_room.rent_place']

        lines = []

        service_queue = list()
        service_queue.append(rent_place_model.search([('id', 'in', service_id)]))

        while len(service_queue):
            current = service_queue.pop()

            if current.children_id:
                service_queue.append(rent_place_model.search([('id', 'in', current.children_id.ids)]))

            for l in current.list_services_id:
                lines.append([0, 0, {
                    'product_id': l.id,
                    'quantity': 1,
                    'specific_price': l.lst_price,
                    'uom_id': l.uom_id.id,
                    'name': 'Renta de local',
                    'automatic_price': False
                }])

        request.env['account.analytic.account'].create({
            'recurring_invoice': False,
            'name': 'Alquiler / %s' % rent_place_model.search([('id', '=', service_id)], limit=1),
            'recurring_invoice_line_ids': lines,
            'is_contract': True,
            'recurrent_invoices': False
        })

        return {"data": {}, "err": False}

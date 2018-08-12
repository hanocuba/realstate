# -*- coding: utf-8 -*-
# /**************************************************************************
# **   CODE LICENCE
# **   Developer: Dairon Domínguez Vega
# **   Date: 12/2/16
# **************************************************************************/
# /*                               __
#  *                            | /  \ |
#  *                           \_\\  //_/
#  *                            .'/()\'.
#  *                             \\  //
#  *
#  *    _/_/_/              _/
#  *   _/    _/    _/_/_/      _/  _/_/    _/_/    _/_/_/
#  *  _/    _/  _/    _/  _/  _/_/      _/    _/  _/    _/
#  * _/    _/  _/    _/  _/  _/        _/    _/  _/    _/
#  *_/_/_/      _/_/_/  _/  _/          _/_/    _/    _/
#  *
#  *
# -*- coding: utf-8 -*-

from functools import wraps
import json

from odoo.http import request, Response, to_jsonable
from odoo.tools.safe_eval import safe_eval


class make_response():

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                if request._request_type == 'json':
                    return to_jsonable(json.dumps(result))
                else:
                    return request.make_response(json.dumps(result))
            except Exception, e:
                if request._request_type == 'json':
                    return to_jsonable({'error': str(e)})
                else:
                    return request.make_response(json.dumps({'error': str(e)}))
        return wrapper


def eval_request_params(kwargs):
    for k, v in kwargs.iteritems():
        try:
            kwargs[k] = safe_eval(v)
        except:
            continue

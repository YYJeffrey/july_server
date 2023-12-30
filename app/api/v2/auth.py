# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
from app.lib.exception import Success
from app.lib.red_print import RedPrint
from app.lib.token import generate_token
from app.service.auth import auth_passive, auth_initiative
from app.validator.forms import PassiveAuthValidator, InitiativeAuthValidator

api = RedPrint('auth')


# @api.route('/token/<user_id>', methods=['GET'])
# def get_tmp_token(user_id):
#     """
#     获取临时令牌
#     """
#     return Success(data=generate_token(user_id=user_id))


@api.route('/passive', methods=['POST'])
def passive():
    """
    被动授权
    """
    form = PassiveAuthValidator()
    user = auth_passive(code=form.get_data('code'))
    return Success(data=user)


@api.route('/initiative', methods=['POST'])
def initiative():
    """
    主动授权
    """
    form = InitiativeAuthValidator()
    user = auth_initiative(**form.dt_data)
    return Success(data=user)

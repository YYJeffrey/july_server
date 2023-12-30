# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
from flask import current_app, g
from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

from .exception import TokenInvalid, TokenExpired, NotFound
from app.model.user import User

auth = HTTPTokenAuth(scheme='Token')


@auth.verify_token
def verify_token(token):
    if hasattr(g, 'user') and  g.user is not None:
        return g.user

    s = Serializer(
        secret_key=current_app.config['SECRET_KEY'],
        expires_in=current_app.config['EXPIRES_IN']
    )
    try:
        data = s.loads(token)
    except BadSignature:
        raise TokenInvalid
    except SignatureExpired:
        raise TokenExpired

    user = User.get_one(id=data['user_id'])
    if user is None:
        raise NotFound(msg='用户不存在')
    g.user = user
    return user


def generate_token(user_id):
    s = Serializer(
        secret_key=current_app.config['SECRET_KEY'],
        expires_in=current_app.config['EXPIRES_IN']
    )
    token = s.dumps({
        'user_id': user_id,
    })
    current_app.logger.info(f"用户生成登录令牌成功, 用户ID: {user_id}")
    return token.decode('ascii')

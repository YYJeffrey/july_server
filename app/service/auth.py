# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
import requests

from app.lib.enums import GenderType
from app.lib.token import generate_token
from app.lib.exception import UserUnInitiativeAuth
from app.manger.qiniu.oss import upload_file
from app.model.user import User
from .mp import get_mp_client


def auth_passive(code):
    """
    被动授权
    """
    client = get_mp_client()
    res = client.login(code)
    openid = res['openid']

    user = User.get_one(openid=openid)
    if user is None:
        raise UserUnInitiativeAuth

    user.token = generate_token(user_id=user.id)
    user.append('token')
    return user


def auth_initiative(code, encrypted_data, iv):
    """
    主动授权
    """
    client = get_mp_client()
    res = client.login(code)
    openid = res['openid']

    user = User.get_one(openid=openid)
    if user is None:
        data = client.decrypt(res['session_key'], encrypted_data, iv)
        gender_dict = {0: GenderType.UN_KNOW, 1: GenderType.MAN, 2: GenderType.WOMAN}
        data['gender'] = gender_dict[data.pop('gender')]
        data['nickname'] = data.pop('nickName')
        data['openid'] = openid

        # 保存头像
        avatar = requests.get(data.pop('avatarUrl')).content
        data['avatar'] = upload_file(path='avatar', data=avatar)
        user = User.create(**data)

    user.token = generate_token(user_id=user.id)
    user.append('token')
    return user

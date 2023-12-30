# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
from flask import current_app

from app.manger.weixin.mp import WeixinMp


def get_mp_client():
    """
    获取微信小程序客户端
    """
    app_id = current_app.config['MP_APP_ID']
    app_secret = current_app.config['MP_APP_SECRET']
    return WeixinMp(app_id=app_id, app_secret=app_secret)

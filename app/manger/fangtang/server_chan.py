# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
import requests
from flask import current_app

TIMEOUT = 30


def send_ft_msg(text, desp):
    """
    Server酱推送消息
    https://sct.ftqq.com
    """
    url = f"https://sctapi.ftqq.com/{current_app.config['SERVER_CHAN_SEND_KEY']}.send"
    data = {'text': text, 'desp': desp}

    try:
        res = requests.post(url=url, data=data, timeout=TIMEOUT).json()
        current_app.logger.info(f"Server酱接口调用成功: {res}")
    except Exception as e:
        current_app.logger.warning(f"Server酱接口调用失败: {e}")

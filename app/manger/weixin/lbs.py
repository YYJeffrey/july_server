# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
import requests
from flask import current_app

TIMEOUT = 30


def ip2region(ip):
    """
    IP地址转地区
    https://lbs.qq.com/service/webService/webServiceGuide/webServiceIp
    """
    url = 'https://apis.map.qq.com/ws/location/v1/ip'
    params = {
        'ip': ip,
        'key': current_app.config['WEIXIN_LBS_KEY']
    }

    try:
        res = requests.get(url=url, params=params, timeout=TIMEOUT).json()
    except Exception as e:
        current_app.logger.error(f"微信LBS接口调用异常: {e}")
        return None

    if res['status'] != 0:
        current_app.logger.error(f"微信LBS接口调用异常: {res}")
        return None

    current_app.logger.info(f"微信LBS接口调用成功: {res}")
    info = res['result']['ad_info']
    if info['province'] == '':
        return info['nation']

    return info['province']

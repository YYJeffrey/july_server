# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
from flask import request, g

from app.manger.weixin.lbs import ip2region


def update_ip_belong():
    """
    更新 IP 归属地: 发布话题、评论时触发
    """
    if request.remote_addr is not None:
        region = ip2region(request.remote_addr)
        if region is not None:
            g.user.update(ip_belong=region)
            return region
    return None

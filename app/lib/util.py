# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
import datetime


def datetime_to_hint(date):
    """
    时间转提示
    """
    now = datetime.datetime.now()
    timedelta = now - date
    seconds = timedelta.days * 86400 + timedelta.seconds
    days = int(seconds / (24 * 60 * 60))
    hours = int(seconds / (60 * 60))
    minutes = int(seconds / 60)

    if days >= 10:
        if now.year == date.year:
            return date.strftime('%m-%d %H:%M')
        return date.strftime('%Y-%m-%d %H:%M')
    elif 10 > days >= 1:
        return str(days) + '天前'
    elif hours >= 1:
        return str(hours) + '小时前'
    elif minutes >= 1:
        return str(minutes) + '分钟前'
    else:
        return '刚刚'

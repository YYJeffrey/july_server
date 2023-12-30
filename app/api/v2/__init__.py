# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
from flask import Blueprint as BluePrint

from . import auth, chat, comment, following, hole, label, message, oss, star, topic, user, video


def create_v2():
    bp = BluePrint('v2', __name__)

    auth.api.register(bp)
    chat.api.register(bp)
    comment.api.register(bp)
    following.api.register(bp)
    hole.api.register(bp)
    label.api.register(bp)
    message.api.register(bp)
    oss.api.register(bp)
    star.api.register(bp)
    topic.api.register(bp)
    user.api.register(bp)
    video.api.register(bp)

    return bp

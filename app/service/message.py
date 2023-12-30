# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
from flask import g
from sqlalchemy.orm import aliased

from app import db
from app.model.message import Message
from app.model.topic import Topic
from app.model.user import User
from app.model.video import Video


def get_message_list():
    """
    查询消息列表
    """
    action_user = aliased(User)

    data = db.session.query(Message, User, action_user, Topic) \
        .outerjoin(User, Message.user_id == User.id) \
        .outerjoin(action_user, Message.action_user_id == action_user.id) \
        .outerjoin(Topic, Message.topic_id == Topic.id) \
        .filter(Message.user_id == g.user.id) \
        .filter(Message.is_read.is_(False)) \
        .filter(Message.delete_time.is_(None)) \
        .all()

    for index, (message, _, message.action_user, message.topic) in enumerate(data):
        if message.topic is not None:
            if message.topic.is_anon and g.user.id != message.topic.user_id:
                message.topic.user = None
            else:
                message.topic.user = User.get_one(id=message.topic.user_id)
            if message.topic.video_id is not None:
                message.topic.video = Video.get_one(id=message.topic.video_id)
            else:
                message.topic.video = None
            message.topic.append('user', 'video')

        if message.is_anon:
            message.action_user = None

        message.append('action_user', 'topic')
        data[index] = message

    return data

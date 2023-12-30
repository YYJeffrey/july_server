# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
from flask import g
from sqlalchemy.orm import aliased

from app import db
from app.lib.enums import MessageCategory
from app.lib.exception import NotFound, Success
from app.model.message import Message
from app.model.star import Star
from app.model.topic import Topic
from app.model.user import User
from app.model.video import Video
from app.validator.forms import PaginateValidator


def get_star_list(topic_id=None, user_id=None):
    """
    获取收藏列表
    """
    validator = PaginateValidator().dt_data
    page = validator.get('page')
    size = validator.get('size')

    topic_user = aliased(User)

    query = db.session.query(Star, Topic, User, topic_user) \
        .outerjoin(Topic, Star.topic_id == Topic.id) \
        .outerjoin(User, Star.user_id == User.id) \
        .outerjoin(topic_user, Topic.user_id == topic_user.id) \
        .filter(Star.delete_time.is_(None))

    if topic_id is not None:
        query = query.filter(Star.topic_id == topic_id)

    if user_id is not None:
        query = query.filter(Star.user_id == user_id)

    data = query.order_by(Star.create_time.desc()).paginate(page=page, size=size)

    items = data.items
    for index, (star, star.topic, star.user, star.topic.user) in enumerate(items):
        if star.topic.is_anon:
            star.topic.user = None
        if star.topic.video_id is not None:
            star.topic.video = Video.get_one(id=star.topic.video_id)
        else:
            star.topic.video = None

        star.append('topic', 'user')
        star.topic.append('user', 'video')
        items[index] = star

    return data


def star_or_cancel_verify(topic_id):
    """
    收藏或取消收藏验证
    """
    topic = Topic.get_one(id=topic_id)
    if topic is None:
        raise NotFound(msg='话题不存在')

    exist_star = Star.get_one(user_id=g.user.id, topic_id=topic.id)
    exist_msg = Message.get_one(category=MessageCategory.STAR, user_id=topic.user_id, action_user_id=g.user.id,
                                topic_id=topic.id, is_read=False)

    # 收藏
    if exist_star is None:
        with db.auto_commit():
            Star.create(commit=False, user_id=g.user.id, topic_id=topic.id)
            if exist_msg is None and topic.user_id != g.user.id:
                Message.create(
                    commit=False,
                    content=MessageCategory.STAR.value + '了你的话题',
                    category=MessageCategory.STAR,
                    user_id=topic.user_id,
                    action_user_id=g.user.id,
                    topic_id=topic.id
                )

        # 更新话题收藏数
        topic.update(star_count=Star.get_star_count(topic_id=topic.id))
        return Success(msg='收藏成功')

    # 取消收藏
    with db.auto_commit():
        exist_star.delete(commit=False)
        if exist_msg is not None:
            exist_msg.delete(commit=False)

    # 更新话题收藏数
    topic.update(star_count=Star.get_star_count(topic_id=topic.id))
    return Success(msg='取消收藏成功')

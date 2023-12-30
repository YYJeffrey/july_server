# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
import datetime

from flask import current_app, g
from sqlalchemy.orm import aliased

from app.lib.enums import MessageCategory
from app.lib.exception import NotFound, TextContentIllegal
from app.model.base import db
from app.model.comment import Comment
from app.model.message import Message
from app.model.topic import Topic
from app.model.user import User
from app.model.video import Video
from app.service.location import update_ip_belong
from app.service.mp import get_mp_client
from app.validator.forms import PaginateValidator


def get_comment_list(topic_id=None, user_id=None):
    """
    获取评论列表
    """
    validator = PaginateValidator().dt_data
    page = validator.get('page')
    size = validator.get('size')

    topic_user = aliased(User)

    query = db.session.query(Comment, Topic, User, topic_user) \
        .outerjoin(Topic, Comment.topic_id == Topic.id) \
        .outerjoin(User, Comment.user_id == User.id) \
        .outerjoin(topic_user, Topic.user_id == topic_user.id) \
        .filter(Comment.delete_time.is_(None)) \
        .filter(Topic.delete_time.is_(None))

    if topic_id is not None:
        query = query.filter(Comment.topic_id == topic_id).order_by(Comment.create_time)

    if user_id is not None:
        query = query.filter(Comment.user_id == user_id).order_by(Comment.create_time.desc())

    data = query.paginate(page=page, size=size)

    items = data.items
    for index, (comment, comment.topic, comment.user, comment.topic.user) in enumerate(items):
        if comment.is_anon:
            comment.user = None
        if comment.topic.is_anon:
            comment.topic.user = None
        if comment.comment_id is not None:
            comment.reply_user = db.session.query(User).outerjoin(Comment, User.id == Comment.user_id) \
                .filter(Comment.id == comment.comment_id).first()
        else:
            comment.reply_user = None
        if comment.topic.video_id is not None:
            comment.topic.video = Video.get_one(id=comment.topic.video_id)
        else:
            comment.topic.video = None

        comment.append('topic', 'user', 'reply_user')
        comment.topic.append('user', 'video')
        items[index] = comment

    return data


def create_comment_verify(form):
    """
    创建评论验证
    """
    # 话题校验
    topic_id = form.get_data('topic_id')
    topic = Topic.get_one(id=topic_id)
    if topic is None:
        raise NotFound(msg='话题不存在')

    # 父评论校验
    comment_id = form.get_data('comment_id')
    if comment_id is not None:
        comment = Comment.get_one(id=comment_id, topic_id=topic_id)
        if comment is None:
            raise NotFound(msg='父评论不存在')
        reply_user_id = comment.user_id
    else:
        reply_user_id = topic.user_id

    # 内容文本校验
    content = form.get_data('content')
    client = get_mp_client()
    if content is not None:
        if not client.check_content(content=content, openid=g.user.openid):
            raise TextContentIllegal('内容不合法')

    # 更新IP归属地
    ip_belong = update_ip_belong()

    # 保存评论和消息 更新话题评论数
    with db.auto_commit():
        comment = Comment.create(commit=False, user_id=g.user.id, ip_belong=ip_belong, **form.dt_data)
        if reply_user_id != g.user.id:
            Message.create(
                commit=False,
                content=MessageCategory.COMMENT.value + '了你',
                category=MessageCategory.COMMENT,
                is_anon=comment.is_anon,
                user_id=reply_user_id,
                action_user_id=g.user.id,
                topic_id=topic.id
            )

    # 更新话题评论数
    topic.update(comment_count=Comment.get_comment_count(topic_id=topic.id))

    # 推送评论消息
    if current_app.config['COMMENT_TEMPLATE_ID'] is not None:
        reply_user = User.get_one(id=reply_user_id)
        send_comment_msg(
            content=content,
            openid=reply_user.openid,
            nickname=g.user.nickname,
            topic_id=topic.id
        )


def send_comment_msg(content, openid, nickname, topic_id):
    """
    推送评论消息
    """
    client = get_mp_client()
    data = {
        'thing2': {'value': content[0:17] + '...' if len(content) > 20 else content},
        'name1': {'value': nickname},
        'time3': {'value': str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}
    }
    client.send_subscribe(
        openid=openid,
        template_id=current_app.config['COMMENT_TEMPLATE_ID'],
        msg_data=data,
        mp_page=f"/pages/topic-detail/index?topicId={topic_id}"
    )

# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
from flask import current_app, g

from app import db
from app.lib.exception import Success, NotFound, Created, Deleted
from app.lib.red_print import RedPrint
from app.lib.schema import paginator_schema
from app.lib.token import auth
from app.manger.fangtang.server_chan import send_ft_msg
from app.model.comment import Comment
from app.model.label import Label
from app.model.star import Star
from app.model.topic import Topic, TopicLabelRel
from app.service.topic import create_topic_verify, format_report_topic, get_topic_list, get_topic_detail
from app.validator.forms import GetTopicListValidator, CreateTopicValidator

api = RedPrint('topic')


@api.route('/<topic_id>', methods=['GET'])
def get_topic(topic_id):
    """
    获取话题详情
    """
    topic = get_topic_detail(topic_id=topic_id)
    if topic is None:
        raise NotFound(msg='话题不存在')

    topic.update(click_count=topic.click_count + 1)
    return Success(data=topic)


@api.route('/', methods=['GET'])
def get_topics():
    """
    获取话题列表
    """
    form = GetTopicListValidator()
    label_id = form.get_data('label_id')
    user_id = form.get_data('user_id')

    # 更新标签点击量
    if label_id is not None:
        label = Label.get_one(id=label_id)
        if label is None:
            raise NotFound(msg='标签不存在')
        label.update(click_count=label.click_count + 1)

    topics = get_topic_list(label_id=label_id, user_id=user_id)
    return Success(data=paginator_schema(topics))


@api.route('/', methods=['POST'])
@auth.login_required
def create_topic():
    """
    发布话题
    """
    form = CreateTopicValidator()
    create_topic_verify(form=form)
    return Created()


@api.route('/<topic_id>', methods=['DELETE'])
@auth.login_required
def delete_topic(topic_id):
    """
    删除话题
    """
    topic = Topic.get_one(id=topic_id)
    if topic is None:
        raise NotFound(msg='话题不存在')

    # 级联删除评论、收藏、关联标签
    with db.auto_commit():
        comments = Comment.get_all(topic_id=topic.id)
        stars = Star.get_all(topic_id=topic.id)
        labels = TopicLabelRel.get_all(topic_id=topic.id)

        for comment in comments:
            comment.delete(commit=False)
        for star in stars:
            star.delete(commit=False)
        for label in labels:
            label.delete(commit=False)

        topic.delete(commit=False)

    return Deleted()


@api.route('/report/<topic_id>', methods=['POST'])
@auth.login_required
def report_topic(topic_id):
    """
    举报话题
    """
    topic = Topic.get_one(id=topic_id)
    if topic is None:
        raise NotFound(msg='话题不存在')

    current_app.logger.warning(f"用户举报话题, 用户ID: {g.user.id}, 用户昵称: {g.user.nickname}, 被举报话题ID: {topic.id}")
    if current_app.config['SERVER_CHAN_SEND_KEY'] is not None:
        send_ft_msg(text='话题举报推送', desp=format_report_topic(topic))
    return Success()

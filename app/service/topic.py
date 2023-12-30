# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
from flask import current_app, g
from sqlalchemy import and_

from app.lib.exception import NotFound, TextContentIllegal, LabelNotAllowedAnonymous, ImagesExceedMaxLength, \
    LabelsExceedMaxLength
from app.lib.enums import VideoStatus
from app.model.base import db
from app.model.label import Label
from app.model.topic import Topic, TopicLabelRel
from app.model.user import User
from app.model.video import Video
from app.validator.forms import PaginateValidator
from .location import update_ip_belong
from .mp import get_mp_client


def get_topic_detail(topic_id):
    """
    获取话题详情
    """
    data = db.session.query(Topic, User, Video) \
        .outerjoin(User, Topic.user_id == User.id) \
        .outerjoin(Video, and_(Topic.video_id == Video.id, Video.video_status == VideoStatus.NORMAL)) \
        .filter(Topic.id == topic_id) \
        .filter(Topic.delete_time.is_(None)) \
        .first()

    topic, topic.user, topic.video = data
    if topic.is_anon:
        topic.user = None
        topic.ip_belong = None

    topic.append('user', 'video', 'starred', 'commented')
    return topic


def get_topic_list(label_id=None, user_id=None):
    """
    获取话题列表
    """
    validator = PaginateValidator().dt_data
    page = validator.get('page')
    size = validator.get('size')

    query = db.session.query(Topic, User, Video) \
        .outerjoin(User, Topic.user_id == User.id) \
        .outerjoin(Video, and_(Topic.video_id == Video.id, Video.video_status == VideoStatus.NORMAL)) \
        .filter(Topic.delete_time.is_(None))

    if label_id is not None:
        topic_ids = db.session.query(TopicLabelRel.topic_id).filter(TopicLabelRel.label_id == label_id)
        query = query.filter(Topic.id.in_(topic_ids))

    if user_id is not None:
        query = query.filter(User.id == user_id)
        # 其他用户不能查看到该用户的匿名话题
        if user_id != g.user.id:
            query = query.filter(Topic.is_anon.is_(False))

    data = query.order_by(Topic.create_time.desc()).paginate(page=page, size=size)

    items = data.items
    for index, (topic, topic.user, topic.video) in enumerate(items):
        if topic.is_anon:
            topic.user = None
            topic.ip_belong = None

        topic.append('user', 'video', 'starred', 'commented')
        items[index] = topic

    return data


def create_topic_verify(form):
    """
    创建话题验证
    """
    # 图片数量校验
    images = form.get_data('images')
    if images is not None:
        if len(images) > current_app.config['MAX_IMAGES_LENGTH']:
            raise ImagesExceedMaxLength

    # 标签数量校验
    labels = form.get_data('labels')
    if labels is not None:
        if len(labels) > current_app.config['MAX_LABELS_LENGTH']:
            raise LabelsExceedMaxLength

    # 视频存在校验
    video_id = form.get_data('video_id')
    if video_id is not None:
        if Video.get_one(id=video_id) is None:
            raise NotFound(msg='视频不存在')

    # 标签匿名校验
    is_anon = form.get_data('is_anon')
    for label_id in labels:
        label = Label.get_one(id=label_id)
        if label is None:
            raise NotFound(msg='标签不存在')
        if is_anon is not None and is_anon and not label.allowed_anon:
            raise LabelNotAllowedAnonymous

    client = get_mp_client()

    # 标题校验
    title = form.get_data('title')
    if title is not None:
        if not client.check_content(content=title, openid=g.user.openid):
            raise TextContentIllegal('标题不合法')

    # 内容校验
    content = form.get_data('content')
    if content is not None:
        if not client.check_content(content=content, openid=g.user.openid):
            raise TextContentIllegal('内容不合法')

    # 更新IP归属地
    ip_belong = update_ip_belong()

    # 保存话题
    with db.auto_commit():
        topic = Topic.create(commit=False, user_id=g.user.id, ip_belong=ip_belong, **form.dt_data)
        db.session.flush()
        labels = form.get_data('labels')
        if labels is not None:
            for label_id in labels:
                TopicLabelRel.create(commit=False, topic_id=topic.id, label_id=label_id)


def format_report_topic(topic):
    """
    格式化举报话题
    """
    image_info = ''
    for image in topic.images:
        image_info += f"![Image]({image})\n"

    # 举报人
    action_user = g.user
    # 被举报人
    user = User.get_one(id=topic.user_id)
    # 被举报视频
    video = Video.get_one(id=topic.video_id)

    return f"**话题ID:** {topic.id}  \n" \
           f"**话题内容:** {topic.content}  \n" \
           f"**被举报人:** {user.nickname}({user.id})  \n" \
           f"**话题图片:** {image_info if image_info != '' else '无'}  \n" \
           f"**举报视频:** {video.src if video else '无'}  \n" \
           f"**举报人:** {action_user.nickname}({action_user.id}) "

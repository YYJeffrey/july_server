# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
from flask import g
from sqlalchemy import Column, String, Integer, Boolean, JSON

from app.lib.util import datetime_to_hint
from .base import BaseModel
from .comment import Comment
from .star import Star


class Topic(BaseModel):
    """
    话题模型
    """
    __tablename__ = 'topic'

    title = Column(String(64), comment='标题')
    content = Column(String(1024), nullable=False, comment='内容')
    is_anon = Column(Boolean, default=False, comment='是否匿名')
    click_count = Column(Integer, default=0, comment='点击次数')
    star_count = Column(Integer, default=0, comment='收藏次数')
    comment_count = Column(Integer, default=0, comment='评论次数')
    images = Column(JSON, comment='图片')
    user_id = Column(String(32), nullable=False, index=True, comment='用户标识')
    video_id = Column(String(32), index=True, comment='视频标识')
    ip_belong = Column(String(128), comment='IP归属地')

    def __str__(self):
        return self.content

    def _set_fields(self):
        self.append('push_time')
        self._exclude.extend(['user_id'])

    @property
    def push_time(self):
        """
        发布时间
        """
        if self.create_time is not None:
            return datetime_to_hint(self.create_time)
        return None

    @property
    def starred(self):
        """
        是否收藏
        """
        if g.user is None:
            return False
        return Star.get_starred(user_id=g.user.id, topic_id=self.id)

    @property
    def commented(self):
        """
        是否评论
        """
        if g.user is None:
            return False
        return Comment.get_commented(user_id=g.user.id, topic_id=self.id)


class TopicLabelRel(BaseModel):
    """
    话题标签关系模型
    """
    __tablename__ = 'topic_label_rel'

    topic_id = Column(String(32), nullable=False, index=True, comment='话题标识')
    label_id = Column(String(32), nullable=False, index=True, comment='标签标识')

    def __str__(self):
        return self.id

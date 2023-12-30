# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
from sqlalchemy import Column, String, Boolean, func

from .base import BaseModel, db
from ..lib.util import datetime_to_hint


class Comment(BaseModel):
    """
    评论模型
    """
    __tablename__ = 'comment'

    content = Column(String(256), nullable=False, comment='内容')
    is_anon = Column(Boolean, default=False, comment='是否匿名')
    user_id = Column(String(32), nullable=False, index=True, comment='用户标识')
    topic_id = Column(String(32), nullable=False, index=True, comment='话题标识')
    comment_id = Column(String(32), index=True, comment='父评论标识')
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

    @classmethod
    def get_commented(cls, user_id, topic_id):
        """
        获取该用户是否评论该话题
        """
        return cls.get_one(user_id=user_id, topic_id=topic_id) is not None

    @classmethod
    def get_comment_count(cls, topic_id):
        """
        获取该话题的评论数量
        """
        return db.session.query(func.count(cls.id)).filter_by(topic_id=topic_id).scalar()

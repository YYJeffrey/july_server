# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
from sqlalchemy import Column, String, Enum, Boolean

from app.lib.enums import MessageCategory
from .base import BaseModel
from ..lib.util import datetime_to_hint


class Message(BaseModel):
    """
    消息模型
    """
    __tablename__ = 'message'

    content = Column(String(256), nullable=False, comment='内容')
    category = Column(Enum(MessageCategory), default=MessageCategory.COMMENT, comment='类型')
    is_read = Column(Boolean, default=False, comment='是否已读')
    is_anon = Column(Boolean, default=False, comment='是否匿名')
    user_id = Column(String(32), nullable=False, index=True, comment='用户标识')
    action_user_id = Column(String(32), nullable=False, index=True, comment='发起用户标识')
    topic_id = Column(String(32), index=True, comment='话题标识')

    def __str__(self):
        return self.content

    def _set_fields(self):
        self.append('push_time')
        self._exclude.extend(['action_user_id'])

    @property
    def push_time(self):
        """
        发布时间
        """
        if self.create_time is not None:
            return datetime_to_hint(self.create_time)
        return None

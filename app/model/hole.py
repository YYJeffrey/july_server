# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
import datetime

from sqlalchemy import Column, String, Boolean, DateTime

from .base import BaseModel
from .chat import Chat
from ..lib.enums import HoleStatus


class Hole(BaseModel):
    """
    树洞模型
    """
    __tablename__ = 'hole'

    title = Column(String(64), nullable=False, comment='标题')
    description = Column(String(512), comment='描述')
    poster = Column(String(256), comment='海报')
    room_id = Column(String(32), nullable=False, comment='房间号')
    allowed_anon = Column(Boolean, default=False, comment='是否可以匿名')
    start_time = Column(DateTime, nullable=False, comment='开始时间')
    end_time = Column(DateTime, nullable=False, comment='结束时间')

    def __str__(self):
        return self.title

    def _set_fields(self):
        self.append('status', 'chat_count')

    @property
    def status(self):
        """
        状态
        """
        now = datetime.datetime.now()
        start = self.start_time
        end = self.end_time

        # 树洞已开启
        if start <= now <= end:
            return HoleStatus.ENABLED

        # 树洞已结束
        elif now > end:
            return HoleStatus.CLOSED

        # 树洞未开启
        else:
            return HoleStatus.UN_ENABLED

    @property
    def chat_count(self):
        """
        动态数量
        """
        return Chat.get_chat_count(room_id=self.room_id)

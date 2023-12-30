# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
from sqlalchemy import Column, String, Enum, func

from .base import BaseModel, db
from app.lib.enums import ChatMessageType


class Chat(BaseModel):
    """
    聊天模型
    """
    __tablename__ = 'chat'

    content = Column(String(512), nullable=False, comment='内容')
    message_type = Column(Enum(ChatMessageType), default=ChatMessageType.TEXT, comment='类型')
    user_id = Column(String(32), nullable=False, index=True, comment='用户标识')
    room_id = Column(String(32), nullable=False, comment='房间号')
    hole_id = Column(String(32), index=True, comment='树洞标识')

    def __str__(self):
        return self.content

    @classmethod
    def get_chat_count(cls, room_id):
        """
        获取该聊天室的动态数
        """
        return db.session.query(func.count(cls.id)).filter_by(room_id=room_id) \
            .filter(cls.message_type != ChatMessageType.INFO).scalar()

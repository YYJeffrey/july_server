# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
from sqlalchemy import Column, String, func

from .base import BaseModel, db


class Star(BaseModel):
    """
    收藏模型
    """
    __tablename__ = 'star'

    user_id = Column(String(32), nullable=False, index=True, comment='用户标识')
    topic_id = Column(String(32), nullable=False, index=True, comment='话题标识')

    def __str__(self):
        return self.id

    @classmethod
    def get_starred(cls, user_id, topic_id):
        """
        获取该用户是否收藏该话题
        """
        return cls.get_one(user_id=user_id, topic_id=topic_id) is not None

    @classmethod
    def get_star_count(cls, topic_id):
        """
        获取该话题的收藏数量
        """
        return db.session.query(func.count(cls.id)).filter_by(topic_id=topic_id).scalar()

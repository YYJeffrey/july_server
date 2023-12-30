# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
from sqlalchemy import Column, String, func

from .base import BaseModel, db


class Following(BaseModel):
    """
    关注模型
    """
    __tablename__ = 'following'

    user_id = Column(String(32), nullable=False, index=True, comment='用户标识')
    follow_user_id = Column(String(32), nullable=False, index=True, comment='被关注用户标识')

    def __str__(self):
        return self.id

    @classmethod
    def get_following_count(cls, user_id):
        """
        获取该用户的关注数量
        """
        return db.session.query(func.count(cls.id)).filter_by(user_id=user_id).scalar()

    @classmethod
    def get_follower_count(cls, follow_user_id):
        """
        获取该用户的被关注数量
        """
        return db.session.query(func.count(cls.id)).filter_by(follow_user_id=follow_user_id).scalar()

    @classmethod
    def get_followed(cls, user_id, follow_user_id):
        """
        获取该用户是否关注指定用户
        """
        return cls.get_one(user_id=user_id, follow_user_id=follow_user_id) is not None

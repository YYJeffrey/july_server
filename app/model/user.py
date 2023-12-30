# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
from sqlalchemy import Column, String, Enum, Boolean

from .base import BaseModel
from app.lib.enums import GenderType


class User(BaseModel):
    """
    用户模型
    """
    __tablename__ = 'user'

    openid = Column(String(64), nullable=False, unique=True, comment='微信openid')
    nickname = Column(String(32), comment='昵称')
    avatar = Column(String(256), comment='头像')
    poster = Column(String(256), comment='封面')
    signature = Column(String(64), comment='个性签名')
    gender = Column(Enum(GenderType), default=GenderType.UN_KNOW, comment='性别')
    city = Column(String(128), comment='城市')
    province = Column(String(128), comment='省份')
    country = Column(String(128), comment='国家')
    ip_belong = Column(String(128), comment='IP归属地')
    is_admin = Column(Boolean, default=False, comment='是否为管理员')
    remark = Column(String(64), comment='备注')

    def __str__(self):
        return self.nickname or self.id

    def _set_fields(self):
        self._exclude.extend(['create_time', 'openid', 'city', 'province', 'country', 'remark'])

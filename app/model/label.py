# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
from sqlalchemy import Column, String, Boolean, Integer

from .base import BaseModel


class Label(BaseModel):
    """
    标签模型
    """
    __tablename__ = 'label'

    name = Column(String(32), nullable=False, comment='名称')
    allowed_anon = Column(Boolean, default=False, comment='是否可以匿名')
    click_count = Column(Integer, default=0, comment='点击次数')
    priority = Column(Integer, default=0, comment='优先级')

    def __str__(self):
        return self.name

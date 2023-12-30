# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
from sqlalchemy import Column, String, Integer, Enum

from .base import BaseModel
from app.lib.enums import VideoStatus


class Video(BaseModel):
    """
    视频模型
    """
    __tablename__ = 'video'

    src = Column(String(256), nullable=False, comment='地址')
    cover = Column(String(256), comment='封面')
    width = Column(Integer, comment='宽度')
    height = Column(Integer, comment='高度')
    duration = Column(Integer, comment='时长')
    size = Column(Integer, comment='大小')
    video_status = Column(Enum(VideoStatus), default=VideoStatus.REVIEWING, comment='状态')
    user_id = Column(String(32), nullable=False, index=True, comment='用户标识')

    def __str__(self):
        return self.src

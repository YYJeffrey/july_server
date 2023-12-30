# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
import logging

from .base import BaseConfig


class ProductionConfig(BaseConfig):
    """
    生产配置
    """
    LOG_LEVEL = logging.INFO
    # 是否启用 SQL 语句回显
    SQLALCHEMY_ECHO = False

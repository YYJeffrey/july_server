# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
import os


class BaseConfig(object):
    """
    基础配置
    """
    # --- 接口相关 ---
    # 请求头校验
    APP_NAME = os.getenv('APP_NAME', 'JULY')
    # 请求头放行的路由
    ALLOWED_PATH = ['*']
    # 是否按 REST 风格返回状态码
    RESTFUL_ENABLE = False

    # --- 应用相关 ---
    # 最大图片数量
    MAX_IMAGES_LENGTH = 9
    # 最大标签数量
    MAX_LABELS_LENGTH = 3
    # 视频审核
    VIDEO_REVIEW = False

    # --- 密钥相关 ---
    SECRET_KEY = os.getenv('SECRET_KEY', 'Hello July')
    EXPIRES_IN = 86400 * 7

    # --- SQLAlchemy 相关 ---
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'SQLALCHEMY_DATABASE_URI',
        'mysql+cymysql://root:123456@127.0.0.1:3306/july?charset=utf8mb4'
    )
    SQLALCHEMY_ENCODING = 'utf8mb4'
    # 是否启用追踪对象修改信号
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 是否启用慢查询记录
    SQLALCHEMY_RECORD_QUERIES = True
    # 连接池选项
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 50,
        'max_overflow': 10,
        'pool_recycle': 1800,
        'pool_timeout': 60,
        'pool_pre_ping': True
    }

    # --- Redis 相关 ---
    REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
    REDIS_PORT = os.getenv('REDIS_PORT', '6379')
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '123456')
    # 存放 ACCESS_TOKEN 的数据库
    REDIS_ACCESS_TOKEN_DB = 7
    # 存放聊天室用户的数据库
    REDIS_CHAT_ROOM_DB = 9

    # --- 微信小程序相关 ---
    MP_APP_ID = os.getenv('MP_APP_ID', 'xxx')
    MP_APP_SECRET = os.getenv('MP_APP_SECRET', 'xxx')
    # 评论订阅消息模板
    COMMENT_TEMPLATE_ID = os.getenv('COMMENT_TEMPLATE_ID', 'xxx')
    # 预约树洞订阅消息模板
    RESERVE_HOLE_TEMPLATE_ID = os.getenv('RESERVE_HOLE_TEMPLATE_ID', 'xxx')

    # --- 七牛云对象存储相关 ---
    QINIU_ACCESS_KEY = os.getenv('QINIU_ACCESS_KEY', 'xxx')
    QINIU_SECRET_KEY = os.getenv('QINIU_SECRET_KEY', 'xxx')
    QINIU_BUCKET_URL = os.getenv('QINIU_BUCKET_URL', 'xxx')
    QINIU_BUCKET_NAME = os.getenv('QINIU_BUCKET_NAME', 'xxx')
    ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'gif', 'png', 'bmp']
    OSS_TOKEN_EXPIRES = 10 * 60

    # --- Server酱相关 ---
    SERVER_CHAN_SEND_KEY = os.getenv('SERVER_CHAN_SEND_KEY', 'xxx')

    # --- 微信 LBS 相关 ---
    WEIXIN_LBS_KEY = os.getenv('WEIXIN_LBS_KEY', 'xxx')

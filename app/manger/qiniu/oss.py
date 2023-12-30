# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
import uuid

from flask import current_app
from qiniu import Auth, put_data

from app.lib.exception import QiniuAPIError


def get_upload_token(key=None):
    """
    七牛云生成上传令牌
    https://developer.qiniu.com/kodo/1242/python
    """
    access_key = current_app.config['QINIU_ACCESS_KEY']
    secret_key = current_app.config['QINIU_SECRET_KEY']
    bucket_name = current_app.config['QINIU_BUCKET_NAME']
    expires = current_app.config['OSS_TOKEN_EXPIRES']

    try:
        auth = Auth(access_key=access_key, secret_key=secret_key)
        return auth.upload_token(bucket=bucket_name, expires=expires, key=key)
    except Exception as e:
        current_app.logger.error(f"七牛云生成上传令牌异常: {e}")
        raise QiniuAPIError


def upload_file(path=None, filename=None, data=None):
    """
    七牛云上传文件
    https://developer.qiniu.com/kodo/1242/python
    """
    bucket_url = current_app.config['QINIU_BUCKET_URL']
    filename = filename or uuid.uuid4().hex
    key = f"{path}/{filename}"
    token = get_upload_token(key=key)

    try:
        put_data(token, key, data)
        return bucket_url + key
    except Exception as e:
        current_app.logger.error(f"七牛云上传文件异常: {e}")
        raise QiniuAPIError

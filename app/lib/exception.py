# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
from flask import json, current_app
from werkzeug.exceptions import HTTPException


class APIException(HTTPException):
    """
    接口异常处理基类
    """
    data = None
    code = 500
    msg_code = 9999
    msg = '服务器未知错误'
    headers = {'Content-Type': 'application/json'}

    def __init__(self, data=None, code=None, msg_code=None, msg=None, headers=None):
        if data:
            self.data = data
        if msg_code:
            self.msg_code = msg_code
        if msg:
            self.msg = msg
        if headers:
            self.headers = headers

        # 状态码返回风格
        if current_app.config['RESTFUL_ENABLE']:
            if code:
                self.code = code
        else:
            self.code = 200

        super(APIException, self).__init__()

    def get_body(self, environ=None):
        body = dict(
            code=self.msg_code,
            msg=self.msg,
            data=self.data
        )
        return json.dumps(body)

    def get_headers(self, environ=None):
        return [(k, v) for k, v in self.headers.items()]


# --- 成功 0~9998 ---
class Success(APIException):
    code = 200
    msg_code = 0
    msg = '成功'


class Created(APIException):
    code = 201
    msg_code = 1
    msg = '创建成功'


class Updated(APIException):
    code = 200
    msg_code = 2
    msg = '更新成功'


class Deleted(APIException):
    code = 200
    msg_code = 3
    msg = '删除成功'


# --- 基础错误 9999~10099 ---
class ServerError(APIException):
    code = 500
    msg_code = 9999
    msg = '服务器未知异常'


class Failed(APIException):
    code = 400
    msg_code = 10000
    msg = '失败'


class ParameterError(APIException):
    code = 400
    msg_code = 10001
    msg = '参数错误'


class Duplicated(APIException):
    code = 400
    msg_code = 10010
    msg = '资源已存在'


class NotFound(APIException):
    code = 404
    msg_code = 10011
    msg = '资源不存在'


class TextContentIllegal(APIException):
    code = 400
    msg_code = 10020
    msg = '文本不合法'


class DataStorageException(APIException):
    code = 400
    msg_code = 10030
    msg = '数据存储异常'


# --- 权限相关 10100~10199 ---
class UnAuthentication(APIException):
    code = 401
    msg_code = 10100
    msg = '未授权访问'


class RequestLimit(APIException):
    code = 401
    msg_code = 10101
    msg = '请求次数超限'


class PasswordInvalid(APIException):
    code = 401
    msg_code = 10110
    msg = '用户名或密码错误'


class TokenInvalid(APIException):
    code = 401
    msg_code = 10120
    msg = 'Token不合法'


class TokenExpired(APIException):
    code = 401
    msg_code = 10121
    msg = 'Token过期'


class AuthorizationInvalid(APIException):
    code = 401
    msg_code = 10122
    msg = 'Authorization不合法'


class HeaderInvalid(APIException):
    code = 401
    msg_code = 10130
    msg = '请求头不合法'


class Forbidden(APIException):
    code = 403
    msg_code = 10140
    msg = '权限不足'


class MethodNotAllowed(APIException):
    code = 405
    msg_code = 10150
    msg = '方法不被允许'


# --- 文件相关 10200~10299 ---
class FileExtensionError(APIException):
    code = 401
    message = '文件后缀名不合法'
    message_code = 10200


class FileTooLarge(APIException):
    code = 413
    msg_code = 10201
    msg = '文件大小超限'


class FileTooMany(APIException):
    code = 413
    msg_code = 10202
    msg = '文件数量超限'


# --- 用户相关 10300~10399 ---
class UserUnInitiativeAuth(APIException):
    code = 400
    msg_code = 10300
    msg = '用户从未主动授权'


# --- 话题相关 10400~10499 ---
class ImagesExceedMaxLength(APIException):
    code = 400
    msg_code = 10400
    msg = '图片超过最大数量'


class LabelsExceedMaxLength(APIException):
    code = 400
    msg_code = 10401
    msg = '标签超过最大数量'


class LabelNotAllowedAnonymous(APIException):
    code = 400
    msg_code = 10402
    msg = '标签不允许匿名'


# --- 关注相关 10500~10599 ---
class FollowingYourselfNotAllowed(APIException):
    code = 400
    msg_code = 10500
    msg = '不允许关注自己'


# --- 树洞相关 10600~10699 ---
class HoleAlreadyEnabled(APIException):
    code = 400
    msg_code = 10600
    msg = '树洞已开启无需预约'


class HoleAlreadyClosed(APIException):
    code = 400
    msg_code = 10601
    msg = '树洞已关闭无法预约'


class HoleUnEnabled(APIException):
    code = 400
    msg_code = 10602
    msg = '树洞未开启'


class HoleReserveRepeated(APIException):
    code = 400
    msg_code = 10602
    msg = '不能重复预约树洞'


# --- 微信相关 20100~20199 ---
class WeixinAPIError(APIException):
    code = 400
    msg_code = 20100
    msg = '微信接口调用异常'


class MpDecryptFailed(APIException):
    code = 400
    msg_code = 20101
    msg = '微信解码失败'


# --- 七牛云相关 20200~20299 ---
class QiniuAPIError(APIException):
    code = 400
    msg_code = 20200
    msg = '七牛云接口调用异常'


class QiniuCallbackError(APIException):
    code = 400
    msg_code = 20201
    msg = '七牛云回调异常'

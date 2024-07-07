# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
import base64
import json

import requests
# noinspection PyPackageRequirements
from Crypto.Cipher import AES
from flask import current_app

from app.lib.exception import WeixinAPIError, MpDecryptFailed

TIMEOUT = 30


class WeixinBase(object):
    """
    微信小程序服务号基类
    """
    base_url = 'https://api.weixin.qq.com'

    def __init__(self, app_id, app_secret, wx_type='mp'):
        """
        wx_type 可选:
        mp: 小程序
        service: 服务号
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.wx_type = wx_type
        self.session_key = None

    def get_access_token(self, grant_type='client_credential'):
        """
        获取 ACCESS_TOKEN 并缓存
        https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/access-token/auth.getAccessToken.html
        """
        access_token_key = f"{self.wx_type}_access_token_{self.app_id}"

        # redis 获取 access_token
        from app import access_token_db
        access_token = access_token_db.get(access_token_key)
        if access_token:
            return access_token

        # 接口请求获取 access_token
        params = {
            'appid': self.app_id,
            'secret': self.app_secret,
            'grant_type': grant_type
        }
        try:
            res = requests.get(url=self.base_url + '/cgi-bin/token', params=params, timeout=TIMEOUT).json()
        except Exception as e:
            current_app.logger.error(f"微信接口调用异常: {e}")
            raise WeixinAPIError

        if 'access_token' not in res:
            current_app.logger.error(f"微信获取access_token失败: {res}")
            raise WeixinAPIError

        access_token = res['access_token']
        access_token_db.set(access_token_key, access_token, res['expires_in'])
        current_app.logger.info(f"微信获取access_token成功: {res}")

        return access_token


class WeixinMp(WeixinBase):
    """
    微信小程序
    """

    def login(self, code, grant_type='authorization_code'):
        """
        登录获取 openid
        https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/login/auth.code2Session.html
        """
        params = {
            'appid': self.app_id,
            'secret': self.app_secret,
            'js_code': code,
            'grant_type': grant_type,
        }
        try:
            res = requests.get(url=self.base_url + '/sns/jscode2session', params=params, timeout=TIMEOUT).json()
        except Exception as e:
            current_app.logger.error(f"微信接口调用异常: {e}")
            raise WeixinAPIError

        if 'openid' not in res:
            current_app.logger.error(f"微信获取openid失败: {res}")
            raise WeixinAPIError

        self.session_key = res['session_key']
        current_app.logger.info(f"微信获取openid成功: {res}")
        return res

    def send_subscribe(self, openid, template_id, msg_data, mp_page=None, mp_state='formal', lang='zh_CN'):
        """
        推送订阅消息
        https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/subscribe-message/subscribeMessage.send.html
        """
        params = {'access_token': self.get_access_token()}
        data = {
            'touser': openid,
            'template_id': template_id,
            'page': mp_page,
            'data': msg_data,
            'miniprogram_state': mp_state,
            'lang': lang
        }
        try:
            res = requests.post(url=self.base_url + '/cgi-bin/message/subscribe/send', params=params, json=data,
                                timeout=TIMEOUT).json()
        except Exception as e:
            current_app.logger.error(f"微信接口调用异常: {e}")
            return

        if res['errcode'] != 0:
            current_app.logger.error(f"微信订阅消息发布失败: {res}")
            return

        current_app.logger.info(f"微信订阅消息发布成功: {res}")

    def check_content(self, content, openid, scene=3):
        """
        内容安全校验
        https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/sec-check/security.msgSecCheck.html
        """
        params = {'access_token': self.get_access_token()}
        data = {
            'content': content.encode('utf-8').decode('latin-1'),
            'openid': openid,
            'version': 2,
            'scene': scene
        }

        try:
            res = requests.post(url=self.base_url + '/wxa/msg_sec_check', params=params,
                                data=json.dumps(data, ensure_ascii=False), timeout=TIMEOUT).json()
        except Exception as e:
            current_app.logger.error(f"微信接口调用异常: {e}")
            raise WeixinAPIError

        if 'errcode' in res and res['errcode'] != 0:
            current_app.logger.error(f"微信内容安全校验异常: {res}")
            raise WeixinAPIError
        if 'suggest' in res['result'] and res['result']['suggest'] != 'pass':
            current_app.logger.warning(f"内容校验发现敏感信息: {res}")
            return False
        return True

    def decrypt(self, session_key, encrypted_data, iv):
        """
        信息解码
        https://developers.weixin.qq.com/miniprogram/dev/framework/open-ability/signature.html
        """
        try:
            session_key = base64.b64decode(session_key)
            encrypted_data = base64.b64decode(encrypted_data)
            iv = base64.b64decode(iv)

            cipher = AES.new(session_key, AES.MODE_CBC, iv)
            decrypted = json.loads(self._un_pad(cipher.decrypt(encrypted_data)))

            if decrypted['watermark']['appid'] != self.app_id:
                current_app.logger.error(f"微信信息解码失败: {decrypted}")
                raise MpDecryptFailed
            return decrypted
        except Exception as e:
            current_app.logger.error(f"微信信息解码异常: {e}")
            raise MpDecryptFailed

    @classmethod
    def _un_pad(cls, s):
        return s[:-ord(s[len(s) - 1:])]

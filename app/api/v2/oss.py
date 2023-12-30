# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
import json

from flask import current_app, g, request

from app.lib.enums import VideoStatus
from app.lib.exception import Success, QiniuCallbackError
from app.lib.red_print import RedPrint
from app.lib.token import auth
from app.manger.qiniu.oss import get_upload_token
from app.model.video import Video

api = RedPrint('oss')


@api.route('/token', methods=['GET'])
@auth.login_required
def get_token():
    """
    获取对象存储上传令牌
    """
    token = get_upload_token()
    current_app.logger.info(f"用户获取OSS令牌成功, 用户ID: {g.user.id}, 用户昵称: {g.user.nickname}")
    return Success(data=token)


@api.route('/callback/video', methods=['POST'])
def callback_video():
    """
    视频审核回调
    https://developer.qiniu.com/censor/5924/video-review-callback
    """
    if request.data is None:
        return Success()

    try:
        data = json.loads(request.data)
        current_app.logger.info(f"视频审核回调成功: {data}")
    except Exception:
        raise QiniuCallbackError

    src = current_app.config['QINIU_BUCKET_URL'] + data['inputKey']
    video = Video.get_one(src=src)

    if video is not None:
        suggestion = data['items'][0]['result']['result']['suggestion']
        if suggestion == 'pass':
            video.update(video_status=VideoStatus.NORMAL)
            current_app.logger.info(f"视频内容正常, 用户ID: {g.user.id}, 用户ID: {video.user_id}")
        else:
            video.update(video_status=VideoStatus.VIOLATION)
            current_app.logger.warning(f"视频内容存在违规, 视频ID: {video.id}, 用户ID: {video.user_id}")

    return Success()

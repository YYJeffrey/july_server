# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
from flask import g, current_app

from app.lib.enums import VideoStatus
from app.lib.exception import Created
from app.lib.red_print import RedPrint
from app.lib.token import auth
from app.model.video import Video
from app.validator.forms import CreateVideoValidator

api = RedPrint('video')


@api.route('/', methods=['POST'])
@auth.login_required
def create_video():
    """
    上传视频
    """
    form = CreateVideoValidator()

    video = Video.create(
        user_id=g.user.id,
        video_status=VideoStatus.REVIEWING if current_app.config['VIDEO_REVIEW'] else VideoStatus.NORMAL,
        **form.dt_data
    )
    return Created(data={'video_id': video.id})

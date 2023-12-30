# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
from flask import g

from app.lib.exception import Success, NotFound, Updated, TextContentIllegal
from app.lib.red_print import RedPrint
from app.lib.token import auth
from app.model.following import Following
from app.model.user import User
from app.service.mp import get_mp_client
from app.validator.forms import UpdateUserValidator

api = RedPrint('user')


@api.route('/<user_id>', methods=['GET'])
@auth.login_required
def get_user(user_id):
    """
    获取用户详情
    """
    user = User.get_one(id=user_id)
    if user is None:
        raise NotFound(msg='用户不存在')

    # 当前用户是否关注指定用户
    user.followed = False if g.user.id == user_id else \
        Following.get_followed(user_id=g.user.id, follow_user_id=user_id)

    # 该用户的关注数量
    user.following_count = Following.get_following_count(user_id=user_id)

    # 该用户的被关注数量
    user.follower_count = Following.get_follower_count(follow_user_id=user_id)

    user.append('followed', 'following_count', 'follower_count')
    return Success(data=user)


@api.route('/', methods=['PUT'])
@auth.login_required
def update_user():
    """
    更新用户信息
    """
    form = UpdateUserValidator()
    user = User.get_one(id=g.user.id)

    client = get_mp_client()
    # 昵称文本校验
    nickname = form.get_data('nickname')
    if nickname is not None and nickname != user.nickname:
        if not client.check_content(content=form.get_data('nickname'), openid=user.openid):
            raise TextContentIllegal('昵称不合法')

    # 个性签名文本校验
    signature = form.get_data('signature')
    if signature is not None and signature != user.signature:
        if not client.check_content(content=form.get_data('signature'), openid=user.openid):
            raise TextContentIllegal('个性签名不合法')

    user.update(**form.dt_data)
    return Updated()

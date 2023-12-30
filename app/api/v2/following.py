# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
from app import auth
from app.lib.exception import Success
from app.lib.red_print import RedPrint
from app.lib.schema import paginator_schema
from app.service.following import follow_or_cancel_verify, get_following_list
from app.validator.forms import FollowOrCancelValidator, GetFollowingListValidator

api = RedPrint('following')


@api.route('/', methods=['GET'])
def get_followings():
    """
    获取关注列表
    """
    form = GetFollowingListValidator()
    user_id = form.get_data('user_id')
    follow_user_id = form.get_data('follow_user_id')

    followings = get_following_list(user_id=user_id, follow_user_id=follow_user_id)
    return Success(data=paginator_schema(followings))


@api.route('/', methods=['POST'])
@auth.login_required
def follow_or_cancel():
    """
    关注或取关
    """
    form = FollowOrCancelValidator()
    return follow_or_cancel_verify(form=form)

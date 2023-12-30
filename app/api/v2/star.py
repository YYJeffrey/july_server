# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
from app import auth
from app.lib.exception import Success
from app.lib.red_print import RedPrint
from app.lib.schema import paginator_schema
from app.service.star import star_or_cancel_verify, get_star_list
from app.validator.forms import StarOrCancelValidator, GetStarListValidator

api = RedPrint('star')


@api.route('/', methods=['GET'])
def get_stars():
    """
    获取收藏列表
    """
    form = GetStarListValidator()
    topic_id = form.get_data('topic_id')
    user_id = form.get_data('user_id')

    stars = get_star_list(topic_id=topic_id, user_id=user_id)
    return Success(data=paginator_schema(stars))


@api.route('/', methods=['POST'])
@auth.login_required
def star_or_cancel():
    """
    收藏或取消收藏
    """
    form = StarOrCancelValidator()
    return star_or_cancel_verify(topic_id=form.get_data('topic_id'))

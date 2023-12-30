# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
from flask import g
from sqlalchemy.orm import aliased

from app.lib.enums import MessageCategory
from app.lib.exception import FollowingYourselfNotAllowed, NotFound, Success
from app.model.base import db
from app.model.following import Following
from app.model.message import Message
from app.model.user import User
from app.validator.forms import PaginateValidator


def get_following_list(user_id=None, follow_user_id=None):
    """
    获取关注列表
    """
    validator = PaginateValidator().dt_data
    page = validator.get('page')
    size = validator.get('size')

    follow_user = aliased(User)

    query = db.session.query(Following, User, follow_user) \
        .outerjoin(User, Following.user_id == User.id) \
        .outerjoin(follow_user, Following.follow_user_id == follow_user.id) \
        .filter(Following.delete_time.is_(None))

    if user_id is not None:
        query = query.filter(Following.user_id == user_id)

    if follow_user_id is not None:
        query = query.filter(Following.follow_user_id == follow_user_id)

    data = query.order_by(Following.create_time.desc()).paginate(page=page, size=size)

    items = data.items
    for index, (following, following.user, following.follow_user) in enumerate(items):
        if user_id is not None:
            following.followed = True
        else:
            following.followed = Following.get_followed(user_id=g.user.id, follow_user_id=follow_user_id)

        following.append('user', 'follow_user', 'followed')
        items[index] = following

    return data


def follow_or_cancel_verify(form):
    """
    关注或取关验证
    """
    follow_user_id = form.get_data('follow_user_id')

    # 被关注者校验
    if follow_user_id == g.user.id:
        raise FollowingYourselfNotAllowed

    user = User.get_one(id=follow_user_id)
    if user is None:
        raise NotFound(msg='用户不存在')

    exist_following = Following.get_one(user_id=g.user.id, follow_user_id=follow_user_id)
    exist_msg = Message.get_one(category=MessageCategory.FOLLOWING, user_id=follow_user_id, action_user_id=g.user.id,
                                is_read=False)

    # 关注
    if exist_following is None:
        with db.auto_commit():
            Following.create(commit=False, user_id=g.user.id, follow_user_id=follow_user_id)
            if exist_msg is None:
                Message.create(
                    commit=False,
                    content=MessageCategory.FOLLOWING.value + '了你',
                    category=MessageCategory.FOLLOWING,
                    user_id=follow_user_id,
                    action_user_id=g.user.id
                )
        return Success(msg='关注成功')

    # 取消关注
    with db.auto_commit():
        exist_following.delete(commit=False)
        if exist_msg is not None:
            exist_msg.delete(commit=False)
    return Success(msg='取关成功')

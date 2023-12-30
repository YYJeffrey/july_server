# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
from flask import g

from app import auth, db
from app.lib.exception import Success, Updated
from app.lib.red_print import RedPrint
from app.model.message import Message
from app.service.message import get_message_list

api = RedPrint('message')


@api.route('/', methods=['GET'])
@auth.login_required
def get_messages():
    """
    获取消息
    """
    messages = get_message_list()
    return Success(data=messages)


@api.route('/read', methods=['POST'])
@auth.login_required
def read_messages():
    """
    已读信息
    """
    with db.auto_commit():
        db.session.query(Message).filter_by(user_id=g.user.id, is_read=False).update({Message.is_read: True})

    return Updated()

# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
from app import db
from app.lib.enums import ChatMessageType
from app.lib.schema import chat_schema
from app.model.chat import Chat
from app.model.user import User
from app.validator.forms import PaginateValidator


def get_chat_list(room_id, chat_id):
    """
    获取聊天列表
    """
    validator = PaginateValidator().dt_data
    page = validator.get('page')
    size = validator.get('size')

    query = db.session.query(Chat, User) \
        .outerjoin(User, Chat.user_id == User.id) \
        .filter(Chat.room_id == room_id) \
        .filter(Chat.message_type != ChatMessageType.INFO) \
        .filter(Chat.delete_time.is_(None))

    # 获取该聊天之前的记录
    if chat_id is not None:
        before_chat = Chat.get_one(id=chat_id)
        query = query.filter(Chat.create_time <= before_chat.create_time) \
            .filter(Chat.id != before_chat.id)

    data = query.order_by(Chat.create_time.desc()).paginate(page=page, size=size)

    items = data.items
    for index, (chat, chat.user) in enumerate(items):
        items[index] = chat_schema(chat=chat, user=chat.user)

    return data

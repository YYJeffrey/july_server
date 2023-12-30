# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
from app.model.chat import Chat
from app.model.user import User
from app.patch.db import Pagination


def paginator_schema(pagination: Pagination):
    """
    分页响应格式
    """
    return {
        'items': pagination.items,
        'current_page': pagination.page,
        'next_page': pagination.next_num,
        'prev_page': pagination.prev_num,
        'total_page': pagination.pages,
        'total_count': pagination.total
    }


def chat_schema(chat: Chat, user: User):
    """
    聊天响应格式
    """
    return {
        'id': chat.id,
        'content': chat.content,
        'message_type': chat.message_type.name,
        'create_time': str(chat.create_time),
        'user': {
            'id': user.id,
            'nickname': user.nickname,
            'avatar': user.avatar,
            'gender': user.gender.name
        }
    }

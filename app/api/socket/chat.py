# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
import json

from flask import session
from flask_socketio import Namespace, join_room, emit, leave_room

from app.lib.enums import HoleStatus, ChatMessageType
from app.lib.exception import NotFound, HoleUnEnabled, TextContentIllegal
from app.lib.schema import chat_schema
from app.model.chat import Chat
from app.model.hole import Hole
from app.service.mp import get_mp_client


class ChatNameSpace(Namespace):
    """
    聊天室命名空间
    """

    @classmethod
    def on_join(cls, data):
        """
        加入房间
        """
        from app import verify_token, chat_room_db

        token = data.get('token')
        room_id = data.get('room_id')
        hole_id = data.get('hole_id')

        # 验证令牌
        user = verify_token(token)

        # 树洞校验
        hole = Hole.get_one(id=hole_id)
        if hole is None:
            raise NotFound(msg='树洞不存在')

        if hole.status != HoleStatus.ENABLED:
            raise HoleUnEnabled

        session['user'] = user
        session['room_id'] = room_id
        session['hole_id'] = hole_id

        # 加入房间
        join_room(room_id)

        # 把用户添加至聊天室集合中
        chat_room_db.sadd(room_id, user.id)

        chat = Chat.create(
            content=f"{user.nickname}进入房间",
            message_type=ChatMessageType.INFO,
            user_id=user.id,
            room_id=room_id,
            hole_id=hole_id
        )
        emit('status', chat_schema(chat=chat, user=user), room=room_id)

    @classmethod
    def on_leave(cls, data):
        """
        离开房间
        """
        from app import chat_room_db

        user = session.get('user')
        room_id = session.get('room_id')
        hole_id = session.get('hole_id')

        # 离开房间
        leave_room(room_id)

        # 把用户从聊天室集合中移除
        chat_room_db.srem(room_id, user.id)

        chat = Chat.create(
            content=f"{user.nickname}离开房间",
            message_type=ChatMessageType.INFO,
            user_id=user.id,
            room_id=room_id,
            hole_id=hole_id
        )
        emit('status', chat_schema(chat=chat, user=user), room=room_id)

    @classmethod
    def on_send(cls, data):
        """
        发送消息
        """
        user = session.get('user')
        room_id = session.get('room_id')
        hole_id = session.get('hole_id')

        data = json.loads(data)
        content = data.get('content')
        message_type = data.get('message_type')

        # 内容校验
        if message_type == ChatMessageType.TEXT.name:
            client = get_mp_client()
            if not client.check_content(content=content, openid=user.openid):
                raise TextContentIllegal('内容不合法')

        chat = Chat.create(
            content=content,
            message_type=message_type,
            user_id=user.id,
            room_id=room_id,
            hole_id=hole_id
        )
        emit('message', chat_schema(chat=chat, user=user), room=room_id)

# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
from flask import current_app, g

from app import scheduler
from app.lib.enums import HoleStatus
from app.lib.exception import NotFound, HoleAlreadyEnabled, HoleAlreadyClosed, Success, HoleReserveRepeated
from app.model.hole import Hole
from app.service.mp import get_mp_client


def reserve_hole_verify(form):
    """
    预约树洞验证
    """
    hole = Hole.get_one(id=form.get_data('hole_id'))
    if hole is None:
        raise NotFound(msg='树洞不存在')

    # 树洞已开启 无需预约
    if hole.status == HoleStatus.ENABLED:
        raise HoleAlreadyEnabled

    # 树洞已结束 无法预约
    elif hole.status == HoleStatus.CLOSED:
        raise HoleAlreadyClosed

    # 树洞未开启 进行预约
    job_id = f"{g.user.id}-{hole.id}"
    exist_job = scheduler.get_job(id=job_id)
    if exist_job is not None:
        raise HoleReserveRepeated

    scheduler.add_job(id=job_id, func=send_reserve_msg, args=(hole, g.user), next_run_time=hole.start_time)
    current_app.logger.info(f"用户预约树洞成功, 用户ID: {g.user.id}, 用户昵称: {g.user.nickname}, 树洞ID: {hole.id}")
    return Success()


def send_reserve_msg(hole, user):
    """
    推送预约消息
    """
    # 调度器独立于 Flask 需要引入上下文环境
    with scheduler.app.app_context():
        client = get_mp_client()
        data = {
            'thing1': {'value': hole.title[0:17] + '...' if len(hole.title) > 20 else hole.title},
            'time2': {'value': str(hole.start_time.strftime('%Y-%m-%d %H:%M:%S'))},
            'thing3': {'value': '你预约的树洞已开启，快来看看吧！'},
            'thing16': {'value': user.nickname}
        }
        client.send_subscribe(
            openid=user.openid,
            template_id=current_app.config['RESERVE_HOLE_TEMPLATE_ID'],
            msg_data=data,
            mp_page=f"/pages/hole-detail/index?holeId={hole.id}"
        )

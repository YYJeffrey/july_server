# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
from app.lib.exception import Success, NotFound
from app.lib.red_print import RedPrint
from app.lib.schema import paginator_schema
from app.model.hole import Hole
from app.service.hole import reserve_hole_verify
from app.validator.forms import ReserveHoleValidator

api = RedPrint('hole')


@api.route('/<hole_id>', methods=['GET'])
def get_hole(hole_id):
    """
    获取树洞详情
    """
    hole = Hole.get_one(id=hole_id)
    if hole is None:
        raise NotFound(msg='树洞不存在')

    return Success(data=hole)


@api.route('/', methods=['GET'])
def get_holes():
    """
    获取树洞列表
    """
    holes = Hole.get_pagination()
    return Success(data=paginator_schema(holes))


@api.route('/reserve', methods=['POST'])
def reserve_hole():
    """
    预约树洞
    """
    form = ReserveHoleValidator()
    return reserve_hole_verify(form=form)

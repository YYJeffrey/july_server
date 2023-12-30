# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
from app import db
from app.model.label import Label
from app.model.topic import TopicLabelRel


def get_label_list(topic_id=None):
    """
    获取标签列表
    """
    query = db.session.query(Label).order_by(Label.priority.desc())

    if topic_id is not None:
        label_ids = db.session.query(TopicLabelRel.label_id).filter(TopicLabelRel.topic_id == topic_id)
        query = query.filter(Label.id.in_(label_ids))

    return query.all()

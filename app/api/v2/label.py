# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
from app.lib.exception import Success
from app.lib.red_print import RedPrint
from app.service.label import get_label_list
from app.validator.forms import GetLabelListValidator

api = RedPrint('label')


@api.route('/', methods=['GET'])
def get_labels():
    """
    获取标签列表
    """
    form = GetLabelListValidator()
    topic_id = form.get_data('topic_id')

    labels = get_label_list(topic_id=topic_id)
    return Success(data=labels)

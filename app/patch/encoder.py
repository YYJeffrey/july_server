# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
from datetime import datetime, date, time
from decimal import Decimal
from enum import Enum

from flask import json
from flask.json import JSONEncoder as _JSONEncoder


class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if isinstance(o, (int, list, set, tuple)):
            return json.dumps(o, cls=JSONEncoder)
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        if isinstance(o, time):
            return o.strftime('%H:%M:%S')
        if isinstance(o, Enum):
            return o.name
        if isinstance(o, Decimal):
            return o.__float__()
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        return JSONEncoder.default(self, o)

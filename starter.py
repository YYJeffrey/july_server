# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
from app import create_app, socketio

app = create_app()

if __name__ == '__main__':
    socketio.run(app, debug=True)

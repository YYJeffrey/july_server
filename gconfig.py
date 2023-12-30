# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
import multiprocessing

from gevent import monkey

monkey.patch_all()

# 是否守护进程
daemon = False
# 是否热部署代码
reload = True
debug = False
bind = '0.0.0.0:5000'
worker_class = 'gevent'
loglevel = 'info'
pidfile = 'log/gunicorn.pid'
accesslog = 'log/access.log'
errorlog = 'log/error.log'
workers = multiprocessing.cpu_count() * 2 + 1

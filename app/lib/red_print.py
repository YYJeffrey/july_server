# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""


class RedPrint(object):
    """
    红图用于嵌套路由使用
    """

    def __init__(self, name):
        self.name = name
        self.mound = []

    def route(self, rule, **options):
        def decorator(func):
            if 'strict_slashes' not in options:
                options['strict_slashes'] = False
            self.mound.append((func, rule, options))
            return func

        return decorator

    def register(self, bp, url_prefix=None):
        if url_prefix is None:
            url_prefix = f"/{self.name}"

        for func, rule, options in self.mound:
            endpoint = f"{self.name}/{options.pop('endpoint', func.__name__)}"
            bp.add_url_rule(url_prefix + rule, endpoint, func, **options)

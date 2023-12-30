# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, Pagination as _Pagination, BaseQuery as _BaseQuery

from app.lib.exception import DataStorageException


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise DataStorageException


class Pagination(_Pagination):
    def hide(self, *keys):
        for item in self.items:
            item.hide(*keys)
        return self

    def append(self, *keys):
        for item in self.items:
            item.append(*keys)
        return self


class BaseQuery(_BaseQuery):
    def filter_by(self, not_del: bool = True, **kwargs):
        """
        查询未被软删除的记录
        """
        if not_del:
            kwargs['delete_time'] = None
        return super(BaseQuery, self).filter_by(**kwargs)

    def paginate(self, page=1, size=20, error_out=True, max_per_page=None):
        """
        覆写分页
        """
        if max_per_page is not None:
            size = min(size, max_per_page)

        items = self.limit(size).offset((page - 1) * size).all()
        total = self.order_by(None).count()

        return Pagination(self, page, size, total, items)

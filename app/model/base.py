# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
from uuid import uuid4

from sqlalchemy import Column, String, DateTime, func, orm, inspect

from app.lib.exception import NotFound
from app.patch.db import SQLAlchemy, BaseQuery
from app.validator.forms import PaginateValidator

db = SQLAlchemy(query_class=BaseQuery)


class BaseModel(db.Model):
    """
    基础模型
    """
    __abstract__ = True

    id = Column('id', String(32), default=lambda: uuid4().hex, primary_key=True, comment='主键标识')
    create_time = Column('create_time', DateTime, server_default=func.now(), index=True, comment='创建时间')
    update_time = Column('update_time', DateTime, onupdate=func.now(), comment='更新时间')
    delete_time = Column('delete_time', DateTime, comment='删除时间')

    def __getitem__(self, key):
        return getattr(self, key)

    @orm.reconstructor
    def init_on_load(self):
        self._fields = ['status']
        self._exclude = ['delete_time', 'update_time']

        self._set_fields()
        self.__set_fields()

    def __set_fields(self):
        columns = inspect(self.__class__).columns
        all_columns = set([column.name for column in columns])
        self._fields.extend(list(all_columns - set(self._exclude)))

    def _set_fields(self):
        """
        子类调用 隐藏和添加字段
        """
        pass

    def keys(self):
        return self._fields

    def hide(self, *keys):
        for key in keys:
            hasattr(self, key) and self._fields.remove(key)
        return self

    def append(self, *keys):
        for key in keys:
            hasattr(self, key) and self._fields.append(key)
        return self

    @property
    def status(self):
        """
        对象状态 是否未删除
        """
        return not self.delete_time

    @classmethod
    def get_or_404(cls, **kwargs):
        rv = cls.query.filter_by(**kwargs).first()
        if not rv:
            raise NotFound
        return rv

    @classmethod
    def all_or_404(cls, **kwargs):
        rv = cls.query.filter_by(**kwargs).all()
        if not rv:
            raise NotFound
        return rv

    @classmethod
    def get_one(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def get_all(cls, **kwargs):
        return cls.query.filter_by(**kwargs).all()

    @classmethod
    def create(cls, commit: bool = True, **kwargs):
        instance = cls()
        instance.init_on_load()
        for attr, value in kwargs.items():
            hasattr(instance, attr) and setattr(instance, attr, value)
        return instance.save(commit)

    def update(self, commit: bool = True, **kwargs):
        for attr, value in kwargs.items():
            hasattr(self, attr) and setattr(self, attr, value)
        return self.save(commit)

    def save(self, commit: bool = True):
        db.session.add(self)
        commit and db.session.commit()
        return self

    def delete(self, commit: bool = True, soft: bool = True):
        """
        删除资源 默认软删除
        """
        if soft:
            self.delete_time = func.now()
            self.save()
        else:
            db.session.delete(self)
        commit and db.session.commit()

    @classmethod
    def get_pagination(cls, not_del: bool = True, **kwargs):
        """
        获取分页数据
        """
        validator = PaginateValidator().dt_data
        page = validator.get('page')
        size = validator.get('size')

        paginator = cls.query
        if not_del:
            kwargs['delete_time'] = None
            paginator = paginator.filter_by(**kwargs)
        return paginator.order_by(cls.create_time.desc()).paginate(page=page, size=size)

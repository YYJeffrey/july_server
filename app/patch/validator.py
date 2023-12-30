# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2023 by Jeffrey.
    :license: Apache 2.0, see LICENSE for more details.
"""
from collections import namedtuple

from flask import request
from wtforms import Form as _Form, SelectField as _SelectField
from wtforms.validators import StopValidation, DataRequired as _DataRequired, Optional as _Optional

from app.lib.exception import ParameterError


class Form(_Form):
    def __init__(self, formdata=None, obj=None, prefix='', meta=None, **kwargs):
        data = request.get_json(silent=True)
        args = request.args.to_dict()
        super().__init__(formdata=formdata, obj=obj, prefix=prefix, data=data, meta=meta, **kwargs, **args)

    def validate_for_api(self):
        """
        处理异常 异常信息拼接
        """
        valid = super(Form, self).validate()
        if not valid:
            msg = ''
            for index, item in enumerate(self.errors.values()):
                msg += ';'.join(item)
                if index != len(self.errors.values()) - 1:
                    msg += ';'
            raise ParameterError(msg=msg)
        return self

    def get_data(self, *args):
        data_list = []
        for arg in args:
            data_list.append(getattr(self._data, arg, None))
        return data_list[0] if len(data_list) == 1 else tuple(data_list)

    @property
    def _data(self):
        self.validate_for_api()
        key_list, value_list = [], []
        for key, value in self._fields.items():
            if value.data is not None:
                key_list.append(key)
                value_list.append(value.data)
        NamedTuple = namedtuple('NamedTuple', [key for key in key_list])
        return NamedTuple(*value_list)

    @property
    def dt_data(self):
        """
        返回 dict 类型
        """
        # noinspection PyProtectedMember
        return self._data._asdict()

    @property
    def nt_data(self):
        """
        返回 namedtuple 类型
        """
        return self._data


class DataRequired(_DataRequired):
    def __call__(self, form, field):
        if field.type == 'IntegerField' and field.data == 0:
            return

        if field.type == 'BooleanField' and field.data is False:
            return

        if not field.data or isinstance(field.data, str) and not field.data.strip():
            if self.message is None:
                message = field.gettext('This field is required.')
            else:
                message = self.message

            field.errors[:] = []
            raise StopValidation(message)


class Optional(_Optional):
    def __call__(self, form, field):
        if field.data:
            return

        if not field.raw_data or isinstance(field.raw_data[0], str) and not self.string_check(
                field.raw_data[0]):
            field.errors[:] = []
            raise StopValidation()


class SelectField(_SelectField):
    def pre_validate(self, form):
        if self.validate_choice:
            for _, _, match in self.iter_choices():
                if match:
                    break
            else:
                raise ValueError(self.gettext('枚举选项有误'))

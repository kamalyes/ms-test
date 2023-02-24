# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.9.11
"""
@File    :  __init__.py
@Time    :  2022/6/17 12:55 AM
@Author  :  YuYanQing
@Version :  1.0
@Contact :  mryu168@163.com
@License :  (C)Copyright 2022-2026
@Desc    :  None
"""
from typing import TypeVar, Callable
from app.core.handler.logger import MsLogger
Transaction = TypeVar("Transaction", bool, Callable)


class MsModelWrapper:

    def __init__(self, model, log=None):
        self.__model__ = model
        if log is None:
            self.__log__ = MsLogger(f"{model.__name__}")
        else:
            self.__log__ = log

    def __call__(self, cls):
        setattr(cls, "__model__", self.__model__)
        setattr(cls, "__log__", self.__log__)
        return cls

    @classmethod
    def obj_to_dic(cls, obj):
        """
        Object转型为dict
        Args:
            obj:

        Returns:
        """
        dic = {}
        for field_key in dir(obj):
            field_value = getattr(obj, field_key)
            if not field_key.startswith("__") and not callable(
                    field_value) and not field_key.startswith("_"):
                dic[field_key] = field_value
        return dic

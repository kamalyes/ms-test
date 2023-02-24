# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.9.11
"""
@File    :  jsonres.py
@Time    :  2022/7/7 15:21 PM
@Author  :  YuYanQing
@Version :  1.0
@Contact :  mryu168@163.com
@License :  (C)Copyright 2022-2026
@Desc    :  None
"""
import os
from datetime import datetime
from decimal import Decimal
from functools import wraps
from json import JSONEncoder
from typing import Union, Any

from fastapi import status, Response, Request
from fastapi.encoders import jsonable_encoder
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse, FileResponse


class MsJsonEncoder(JSONEncoder):

    def default(self, o: Any) -> Any:
        if isinstance(o, set):
            return list(o)
        if isinstance(o, datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(o, Decimal):
            return str(o)
        if isinstance(o, bytes):
            return o.decode(encoding='utf-8')
        return self.default(o)


class MsResponse:
    def __init__(self):
        pass

    @staticmethod
    def model_to_dict(obj, *ignore: str):
        """
        将orm模型转换为dict
        Args:
            obj:
            *ignore:

        Returns:

        """
        if getattr(obj, '__table__', None) is None:
            return obj
        result = dict()
        for c in obj.__table__.columns:
            if c.name in ignore:
                # 如果字段忽略, 则不进行转换
                continue
            val = getattr(obj, c.name)
            if isinstance(val, datetime):
                result[c.name] = val.strftime("%Y-%m-%d %H:%M:%S")
            else:
                result[c.name] = val
        return result

    @staticmethod
    def json_serialize(obj):
        """
        json序列化
        Args:
            obj:

        Returns:

        """
        ans = dict()
        for k, o in dict(obj).items():
            if isinstance(o, set):
                ans[k] = list(o)
            elif isinstance(o, datetime):
                ans[k] = o.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(o, Decimal):
                ans[k] = str(o)
            elif isinstance(o, bytes):
                ans[k] = o.decode(encoding='utf-8')
            else:
                ans[k] = o
        return ans

    @staticmethod
    def dict_model_to_dict(obj):
        for k, v in obj.items():
            if isinstance(v, dict):
                MsResponse.dict_model_to_dict(v)
            elif isinstance(v, list):
                obj[k] = MsResponse.model_to_list(v)
            else:
                obj[k] = MsResponse.model_to_dict(v)
        return obj

    @staticmethod
    def parse_sql_result(data: list):
        columns = []
        if len(data) > 0:
            columns = list(data[0].keys())
        return columns, [MsResponse.json_serialize(obj) for obj in data]

    @staticmethod
    def model_to_list(data: list, *ignore: str):
        return [MsResponse.model_to_dict(x, *ignore) for x in data]

    @staticmethod
    def encode_json(data: Any, *exclude: str):
        return jsonable_encoder(data, exclude=exclude, custom_encoder={
            datetime: lambda x: x.strftime("%Y-%m-%d %H:%M:%S")
        })

    @staticmethod
    def records(data: list, code=status.HTTP_200_OK, message="操作成功"):
        return dict(code=code, message=message, data=MsResponse.model_to_list(data))

    @staticmethod
    def success(data=None, code=status.HTTP_200_OK, message="操作成功", exclude=()):
        return MsResponse.encode_json(dict(code=code, message=message, data=data), *exclude)

    @staticmethod
    def success_with_size(
            *,
            code: Union[int, str] = status.HTTP_200_OK,
            status_code: Union[int, str] = status.HTTP_200_OK,
            data: Union[list, dict, str] = None,
            total: Union[list, dict, str] = None,
            message: str = "Success",
    ) -> Response:
        """
        响应成功 应用列表
        Args:
            code:
            status_code:
            data:
            total:
            message:

        Returns:

        """
        return JSONResponse(
            status_code=status_code,
            content=jsonable_encoder(
                {
                    "code": code,
                    "message": message,
                    "data": data,
                    "total": total,
                }
            ),
        )

    @staticmethod
    def failed(
            *,
            code: Union[int, str] = status.HTTP_500_INTERNAL_SERVER_ERROR,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail: str = "Internal Server Error",
            data: Union[list, dict, str] = None
    ) -> Response:
        """
        失败返回
        Args:
            code:
            status_code:
            detail:
            data:

        Returns:

        """
        return JSONResponse(
            status_code=status_code,
            content=jsonable_encoder(
                {"code": code, "detail": detail, "data": data}),
        )

    @staticmethod
    def custom(
            *,
            code: Union[int, str] = status.HTTP_201_CREATED,
            status_code: Union[int, str] = status.HTTP_201_CREATED,
            detail: str = "",
    ) -> Response:
        """
        自定义返回值
        Args:
            code:
            status_code:
            detail:

        Returns:

        """
        return JSONResponse(
            status_code=status_code,
            content=jsonable_encoder(
                {
                    "code": code,
                    "detail": detail,
                }
            ),
        )

    @staticmethod
    def file(filepath, filename):
        return FileResponse(filepath, filename=filename,
                            background=BackgroundTask(lambda: os.remove(filepath)))

    @staticmethod
    def forbidden():
        return dict(code=403, msg="对不起, 你没有权限")


def json_required(func):
    """
    此装饰器可以装饰所有post请求 避免处理非json数据报错
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        json_dict = Request.json()
        if json_dict is None:
            return MsResponse.failed(code=400, detail='json is required')
        return func(*args, **kwargs)

    return wrapper

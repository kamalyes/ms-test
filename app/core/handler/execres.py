# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.9.11
"""
@File    :  execres.py
@Time    :  2022/7/7 15:21 PM
@Author  :  YuYanQing
@Version :  1.0
@Contact :  mryu168@163.com
@License :  (C)Copyright 2022-2026
@Desc    :  None
"""

from fastapi import HTTPException, status

class PermissionException(HTTPException):
    pass


class ValidException(Exception):
    def __init__(
            self,
            code: int = 422,
            status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail: str = "Parameter effect error",
    ):
        self.code = code
        self.detail = detail
        self.status_code = status_code


class AuthException(Exception):
    def __init__(
            self,
            code: int = 401,
            detail: str = "Authentication failed",
            status_code: int = status.HTTP_401_UNAUTHORIZED,
    ):
        self.code = code
        self.detail = detail
        self.status_code = status_code


class AccessException(Exception):
    def __init__(
            self,
            code: int = 403,
            detail: str = "Access failed",
            status_code: int = status.HTTP_403_FORBIDDEN,
    ):
        self.code = code
        self.detail = detail
        self.status_code = status_code


class ThirdException(Exception):
    def __init__(
            self,
            code: int = 500,
            detail: str = "Third Service Exception",
            status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ):
        self.code = code
        self.detail = detail
        self.status_code = status_code

class SystemException(Exception):
    def __init__(
            self,
            code: int = 500,
            detail: str = "Operation System Exception",
            status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ):
        self.code = code
        self.detail = detail
        self.status_code = status_code

# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.9.11
"""
@File    :  __init__.py
@Time    :  2022/7/7 15:21 PM
@Author  :  YuYanQing
@Version :  1.0
@Contact :  mryu168@163.com
@License :  (C)Copyright 2022-2026
@Desc    :  None
"""

from fastapi import Depends
from app.core.handler.execres import AuthException

from app.schema.kerberos import OAuth2TokenSchema


FORBIDDEN = "对不起, 你没有足够的权限"


class Permission:

    async def __call__(self, request: OAuth2TokenSchema = Depends()):
        if request.kerberos_code != "688123":
          raise AuthException(detail=FORBIDDEN)

# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.9.11
"""
@File    :  kerberos.py
@Time    :  2022/7/7 15:21 PM
@Author  :  YuYanQing
@Version :  1.0
@Contact :  mryu168@163.com
@License :  (C)Copyright 2022-2026
@Desc    :  None
"""
import time
import jwt

from app.curl.awen.kerberos import KerberosDao
from app.schema.kerberos import KerberosSchema


class Kerberos():
    async def generate_awen_token(request: KerberosSchema):
       return await KerberosDao.generate_awen_token(request)

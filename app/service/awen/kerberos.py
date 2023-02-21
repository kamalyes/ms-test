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

from fastapi import APIRouter, Depends

from app.curl.awen.kerberos import KerberosDao
from app.schema.kerberos import EnvironmentSchema, KerberosSchema
from app.service import Permission

router = APIRouter()


@router.post("/awtoken/generate", summary="生成阿闻后台token")
async def generate_awen_token(request: KerberosSchema, oauth=Depends(Permission())):
  return await KerberosDao.generate_awen_token(request)
  
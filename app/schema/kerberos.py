# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.9.11
"""
@File    :  user.py
@Time    :  2022/7/7 15:21 PM
@Author  :  YuYanQing
@Version :  1.0
@Contact :  mryu168@163.com
@License :  (C)Copyright 2022-2026
@Desc    :  None
"""

from typing import Optional

from fastapi import Body, Header
from pydantic import BaseModel


class OAuth2TokenSchema:
    def __init__(
            self,
            kerberos_code: Optional[str] = Header(None, title="kerberos_code", max_length=600)
    ):
        self.kerberos_code = kerberos_code

class EnvironmentSchema(BaseModel):
  env: Optional[int] = Body(0, title="env")

class KerberosSchema(EnvironmentSchema):
  userno: Optional[str] = Body("", title="userno")
  mobile: Optional[str] = Body("", title="mobile")
  name: Optional[str] = Body("", title="name")
  exp: Optional[int] = Body(72, title="exp")
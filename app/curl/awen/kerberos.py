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
from app.core.handler.execres import ValidException
from app.core.handler.jsonres import MsResponse

from app.curl import MsModelWrapper
from app.schema.kerberos import KerberosSchema
from config import MsAppConfig
from custard.time import Moment
from app.core.handler._cacheout import cache
@MsModelWrapper(KerberosSchema)
class KerberosDao():

    @classmethod
    async def generate_awen_token(cls, request: KerberosSchema):
        """_summary_
        Args:
            request (KerberosSchema): _description_ { "mobile": 18176699611,"name": "yu","userno": "U_3B63GEA","exp": 1677577765, "env":1}
        Raises:
            ValidException: _description_
        Returns:
            _type_: _description_
        """
        valid_env_array_, env_, userno, ttl = {1: "sit", 2: "uat"}, request.env, request.userno, request.ttl
        old_token = cache.get(userno)
        if old_token is not None:
            token = old_token
        elif env_ in valid_env_array_:
            private_key_path = f"{MsAppConfig.CONF_PATH}/{valid_env_array_.get(env_)}_private_key.pem"
            claims = {
                "mobile": request.mobile,
                "name": request.name,
                "userno": request.userno
            }
            exp = int(time.mktime(time.strptime(Moment.skew_date(hours=request.exp), "%Y-%m-%d %H:%M:%S")))
            claims['exp'] = exp
            secret = open(private_key_path, "rb").read()
            token = jwt.encode(claims, secret, algorithm='RS256')
            cache.set(userno, token, ttl=ttl)
        else:
            raise ValidException
        return MsResponse.success(data={"token": token})

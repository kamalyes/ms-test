# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.9.11
"""
@File    :  cacheout.py
@Time    :  2022/7/7 15:21 PM
@Author  :  YuYanQing
@Version :  1.0
@Contact :  mryu168@163.com
@License :  (C)Copyright 2022-2026
@Desc    :  None
"""
import time
from cacheout import Cache
cache = Cache(maxsize=256, ttl=0, timer=time.time, default=None) 

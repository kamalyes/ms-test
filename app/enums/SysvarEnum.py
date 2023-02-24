# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.9.11
"""
@File    :  SysvarEnum.py
@Time    :  2022/7/7 15:21 PM
@Author  :  YuYanQing
@Version :  1.0
@Contact :  mryu168@163.com
@License :  (C)Copyright 2022-2026
@Desc    :  None
"""
from enum import IntEnum, Enum

from custard.time import Moment


class MsGlobalVarEnum:
    BANNER = r"""
         ____        __                  
        /\  _`\   __/\ \                 
        \ \ \L\ \/\_\ \ \/'\      __     
         \ \ ,__/\/\ \ \ , <    /'__`\   
          \ \ \/  \ \ \ \ \\`\ /\ \L\.\_ 
           \ \_\   \ \_\ \_\ \_\ \__/.\_\
            \/_/    \/_/\/_/\/_/\/__/\/_/
        """
    BIG_HUMP_APP_NAME = "Ms"
    VERIFY_CODE_WHITE_LIST = ("888888", "Sweet")
    
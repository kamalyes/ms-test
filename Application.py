# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.9.11
"""
@File    :  Application.py
@Time    :  2021/10/18 2:28 AM
@Author  :  YuYanQing
@Version :  1.0
@Contact :  mryu168@163.com
@License :  (C)Copyright 2022-2026
@Desc    :  总程序
"""
import traceback
import uvicorn
from fastapi import FastAPI, Request, status, Depends
from custard.core import System
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.responses import Response
from app.core.handler.execres import AccessException, AuthException, SystemException, ValidException
from app.core.handler.jsonres import MsResponse

from app.service.awen import kerberos_router
from config import MsAppConfig, InterceptHandler

logger = InterceptHandler.init_logging()


class MsFastApi:

    @staticmethod
    async def request_info(request: Request):
        logger.bind(name=None).info(f"{request.method} {request.url}")
        try:
            body = await request.json()
            logger.bind(payload=body, name=None).debug("request_json: ")
        except Exception as e:
            try:
                body = await request.body()
                if len(body) != 0:
                    # 有请求体，记录日志
                    logger.bind(payload=body, name=None).debug(body)
            except Exception as e:
                # 忽略文件上传类型的数据
                pass

    @staticmethod
    def register_exc(app: FastAPI):
        """
        捕获异常
        Args:
            app:

        Returns:

        """

        @app.exception_handler(ValidException)
        async def valid_exc_handler(request: Request, exc: ValidException):
            """
            参数错误
            Args:
                request:
                exc:

            Returns:

            """
            return MsResponse.custom(code=exc.code, status_code=exc.status_code,
                                     detail=exc.detail)

        @app.exception_handler(AuthException)
        async def auth_exc_handler(request: Request, exc: AuthException) -> Response:
            """
            鉴权异常
            Args:
                request:
                exc:

            Returns:

            """
            return MsResponse.custom(code=exc.code, status_code=exc.status_code,
                                     detail=exc.detail)

        @app.exception_handler(SystemException)
        async def sys_exc_handler(request: Request, exc: SystemException) -> Response:
            """
            系统异常
            Args:
                request:
                exc:

            Returns:

            """
            return MsResponse.custom(code=exc.code, status_code=exc.status_code,
                                     detail=exc.detail)

        @app.exception_handler(AccessException)
        async def access_exc_handler(request: Request, exc: AccessException) -> Response:
            """
            访问失败
            Args:
                request:
                exc:

            Returns:

            """
            return MsResponse.custom(code=exc.code, status_code=exc.status_code,
                                     detail=exc.detail)

        @app.exception_handler(Exception)
        async def all_exc_handler(request: Request, exc: Exception) -> Response:
            """
            全局所有异常
            Args:
                request:
                exc:

            Returns:

            """
            error_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return MsResponse.custom(code=error_code, status_code=error_code,
                                     detail=traceback.format_exc())

    # noinspection PyShadowingNames
    @staticmethod
    def create_app(origins=None, title=f"测试平台",
                   requirements=None):
        """
        初始化app、配置路由及swagger
        Args:
            app_name:
            origins:
            title:
            requirements:
        Returns:
        """
        requirements = requirements if requirements else MsAppConfig.REQUIREMENTS
        Ms = FastAPI(
            title=title,
            description=f"""
    - 后端: requirements: {requirements}
    - 运行环境：{System.get_platform_info()}""",
            version="0.0.1",
            openapi_url="/openapi.json",
            docs_url="/docs",
        )
        origins = [origins]
        #  解决跨域问题
        Ms.add_middleware(
            CORSMiddleware,  # 强制所有传入请求都具有正确设置的Host标头，以防止 HTTP 主机标头攻击。
            allow_origins=origins,  # 允许访问的源
            allow_origin_regex="https?://.*",
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        Ms.add_middleware(TrustedHostMiddleware,
                          allowed_hosts=["localhost", "*"])
        # 处理包含"gzip"在Accept-Encoding标头中的任何请求的 GZip响应
        Ms.add_middleware(GZipMiddleware, minimum_size=1000)

        # 注册捕获全局异常
        MsFastApi.register_exc(Ms)
        # 注册路由
        Ms.include_router(kerberos_router, prefix="/kerberos", tags=["kerberos"],
                          dependencies=[Depends(MsFastApi.request_info)])
        return Ms


Ms = MsFastApi.create_app()


if __name__ == "__main__":
    uvicorn.run(
        app="Application:Ms",
        host=MsAppConfig.SERVER_HOST,
        port=MsAppConfig.SERVER_PORT,
        reload=True
    )

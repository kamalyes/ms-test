# 基础配置类
import logging
from pprint import pformat
import sys
import os
import time
from loguru import logger
from pydantic import BaseSettings
from loguru._defaults import LOGURU_FORMAT
from custard.core import System


ROOT = os.path.dirname(os.path.abspath(__file__))


class BaseConfig(BaseSettings):
    # System
    ENVIRONMENT: str = "dev"
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 7777
    WORKSPACES_PATH: str = os.path.dirname(os.path.abspath(__file__))
    LOWER_HUMP_APP_NAME: str = "auto-test"
    # 日志相关
    LOGS_DIR_NAME = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    LOGS_PATH: str = f"{WORKSPACES_PATH}/logs"
    CONF_PATH: str = f"{WORKSPACES_PATH}/conf"
    LOG_GENERAL_DIR = os.path.join(LOGS_PATH, LOGS_DIR_NAME)
    INFO_LOG_FILE = os.path.join(LOG_GENERAL_DIR,
                                 f"{LOWER_HUMP_APP_NAME}-info.log")
    ERROR_LOG_FILE = os.path.join(LOG_GENERAL_DIR,
                                  f"{LOWER_HUMP_APP_NAME}-error.log")
    REQUIREMENTS: str = System.get_depend_libs(
        file_path=f"{WORKSPACES_PATH}/requirements.txt"
    )
    # 配置日志格式
    INFO_FORMAT = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> "
        "| <level>{level: <8}</level> | <cyan>文件: {extra[filename]}</cyan> \n"
        "| 模块: <cyan>{extra[business]}</cyan> | 方法: <cyan>{extra[func]}</cyan> "
        "| <cyan>行数: {extra[line]}</cyan> | - <level>{message}</level>"
    )

    ERROR_FORMAT = (
        "<red>{time:YYYY-MM-DD HH:mm:ss.SSS}</red> "
        "| <level>{level: <8}</level> | <cyan>文件: {extra[filename]}</cyan> \n"
        "| 模块: <cyan>{extra[business]}</cyan> | 方法: <cyan>{extra[func]}</cyan> "
        "| <cyan>行数: {extra[line]}</cyan> | - <level>{message}</level>"
    )


class EnvConfig(BaseConfig):
    class Config:
        env_file = os.path.join(ROOT, "conf", ".env")


MsAppConfig = EnvConfig()
MsAppConfig.ENVIRONMENT = os.environ.get("MS_ENV", "dev")


class InterceptHandler(logging.Handler):
    """
    Default handler from examples in loguru documentaion.
    See https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
    """

    def emit(self, record: logging.LogRecord):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )

    @staticmethod
    def make_filter(name):
        # 过滤操作，当日志要选择对应的日志文件的时候，通过filter进行筛选
        def filter_(record):
            return record["extra"].get("name") == name

        return filter_

    @staticmethod
    def format_record(record: dict) -> str:
        """
        这里的代码是copy的，记录日志格式的
        Custom format for loguru loggers.
        Uses pformat for log any data like request/response body during debug.
        Works with logging if loguru handler it.
        Example:
        # >>> payload = [{"users":[{"name": "Nick", "age": 87, "is_active": True}, {"name": "Alex", "age": 27, "is_active": True}], "count": 2}]
        # >>> log.bind(payload=).debug("users payload")
        # >>> [   {   'count': 2,
        # >>>         'users': [   {'age': 87, 'is_active': True, 'name': 'Nick'},
        # >>>                      {'age': 27, 'is_active': True, 'name': 'Alex'}]}]
        """

        format_string = LOGURU_FORMAT
        if record["extra"].get("payload") is not None:
            record["extra"]["payload"] = pformat(
                record["extra"]["payload"], indent=4, compact=True, width=88
            )
            format_string += "\n<level>{extra[payload]}</level>"

        format_string += "{exception}\n"
        return format_string

    @staticmethod
    def init_logging():
        loggers = (
            logging.getLogger(name)
            for name in logging.root.manager.loggerDict
            if name.startswith("uvicorn.")
        )
        for uvicorn_logger in loggers:
            uvicorn_logger.handlers = []

        # 这里的操作是为了改变uvicorn默认的logger，使之采用loguru的logger
        # change handler for default uvicorn log
        intercept_handler = InterceptHandler()
        logging.getLogger("uvicorn").handlers = [intercept_handler]
        # logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
        # logging.basicConfig(level=logging.INFO)
        logger.add(
            MsAppConfig.INFO_LOG_FILE,
            enqueue=True,
            rotation="20 MB",
            level="DEBUG",
            filter=InterceptHandler.make_filter(MsAppConfig.INFO_LOG_FILE),
        )

        logger.add(
            MsAppConfig.ERROR_LOG_FILE,
            enqueue=True,
            rotation="10 MB",
            level="WARNING",
            filter=InterceptHandler.make_filter(MsAppConfig.ERROR_LOG_FILE),
        )

        # 配置loguru的日志句柄，sink代表输出的目标
        logger.configure(
            handlers=[
                {
                    "sink": sys.stdout,
                    "level": logging.DEBUG,
                    "format": InterceptHandler.format_record,
                },
                {
                    "sink": MsAppConfig.INFO_LOG_FILE,
                    "level": logging.INFO,
                    "format": MsAppConfig.INFO_FORMAT,
                    "filter": InterceptHandler.make_filter(MsAppConfig.INFO_LOG_FILE),
                },
                {
                    "sink": MsAppConfig.ERROR_LOG_FILE,
                    "level": logging.WARNING,
                    "format": MsAppConfig.ERROR_FORMAT,
                    "filter": InterceptHandler.make_filter(
                        MsAppConfig.ERROR_LOG_FILE
                    ),
                },
            ]
        )
        return logger

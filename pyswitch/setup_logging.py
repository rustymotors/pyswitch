import sys
from loguru import logger


import inspect
import logging


def setup_logging(DEFAULT_LOGGING_LEVEL):
    logger.remove()
    logger.add("logs/pyswitch.log", level=DEFAULT_LOGGING_LEVEL)
    logger.add(sys.stderr, level="ERROR")
    logger.add(sys.stdout, level=DEFAULT_LOGGING_LEVEL)

    class InterceptHandler(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            # Get corresponding Loguru level if it exists.
            level: str | int
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            # Find caller from where originated the logged message.
            frame, depth = inspect.currentframe(), 0
            while frame and (
                depth == 0 or frame.f_code.co_filename == logging.__file__
            ):
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage()
            )

    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

import sys
from typing import TYPE_CHECKING

from loguru import logger
from src.config import settings_factory

if TYPE_CHECKING:
    from loguru import Logger
else:
    Logger = None


def logger_factory() -> Logger:
    logger.remove()
    settings = settings_factory()

    log_level = "DEBUG" if settings.DEBUG else "INFO"

    logger.add(
        sys.stdout,
        level=log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{file}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True,
    )

    logger.level("INFO", color="<green>")
    logger.level("DEBUG", color="<yellow>")
    logger.level("ERROR", color="<red>")

    return logger

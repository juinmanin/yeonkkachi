"""
logger.py – Centralised logging for the Yeonkkachi trading bot.

All components import get_logger() and use the returned logger
so that output is consistent and written to both the console and
a rotating log file under logs/.
"""

import os
import sys
from loguru import logger


LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "yeonkkachi_{time:YYYY-MM-DD}.log")

# Remove the default sink then add our own.
logger.remove()

# Human-readable console output.
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> – {message}",
    level="INFO",
    colorize=True,
)

# Daily rotating file output retained for 30 days.
logger.add(
    LOG_FILE,
    rotation="00:00",
    retention="30 days",
    compression="zip",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} – {message}",
    level="DEBUG",
    enqueue=True,
)


def get_logger(name: str = "yeonkkachi"):
    """Return a logger bound to *name* for contextual log messages."""
    return logger.bind(name=name)

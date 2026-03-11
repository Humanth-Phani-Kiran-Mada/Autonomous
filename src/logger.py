"""
Advanced logging system for the AI system
"""
import sys
from loguru import logger
from pathlib import Path
import config

# Remove default handler
logger.remove()

# Add console handler with colors
logger.add(
    sys.stderr,
    format="<level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level=config.LOG_LEVEL,
    colorize=True,
)

# Add file handler
log_file = config.LOGS_DIR / "ai_evolution.log"
logger.add(
    str(log_file),
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level=config.LOG_LEVEL,
    rotation="500 MB",
    retention="30 days",
)

# Add error file handler
error_file = config.LOGS_DIR / "errors.log"
logger.add(
    str(error_file),
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="ERROR",
    rotation="500 MB",
    retention="90 days",
)

__all__ = ["logger"]

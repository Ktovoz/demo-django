from loguru import logger
import sys
import os
from pathlib import Path

# 创建logs目录（如果不存在）
LOGS_DIR = Path(__file__).resolve().parent.parent / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

# 移除默认的日志处理器
logger.remove()

# 添加标准输出处理器
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    enqueue=True,  # 异步写入
)

# 添加文件处理器
logger.add(
    LOGS_DIR / "django.log",
    rotation="500 MB",  # 日志文件最大500MB
    retention="30 days",  # 保留30天的日志
    compression="zip",  # 压缩旧日志
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    enqueue=True,  # 异步写入
)

# 添加错误日志处理器
logger.add(
    LOGS_DIR / "error.log",
    level="ERROR",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    enqueue=True,  # 异步写入
    backtrace=True,  # 错误回溯
    diagnose=True,  # 详细诊断信息
)
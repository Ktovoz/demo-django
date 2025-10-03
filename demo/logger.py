from loguru import logger
import sys
import os
from pathlib import Path

# 创建logs目录（如果不存在）
LOGS_DIR = Path(__file__).resolve().parent.parent / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

# 移除默认的日志处理器
logger.remove()

# 添加标准输出处理器（控制台输出）
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    enqueue=True,  # 异步写入
)

# 添加应用日志处理器（包含所有应用操作）
logger.add(
    LOGS_DIR / "django.log",
    rotation="500 MB",  # 日志文件最大500MB
    retention="30 days",  # 保留30天的日志
    compression="zip",  # 压缩旧日志
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    enqueue=True,  # 异步写入
)

# 添加安全日志处理器（专门记录安全相关操作）
logger.add(
    LOGS_DIR / "security.log",
    rotation="100 MB",  # 安全日志文件较小，便于监控
    retention="90 days",  # 安全日志保留更长时间
    compression="zip",
    level="INFO",  # 记录INFO级别以上的安全日志
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | SECURITY | {name}:{function}:{line} - {message}",
    enqueue=True,
    filter=lambda record: "SECURITY" in record["message"] or
                         "登录" in record["message"] or
                         "权限" in record["message"] or
                         "初始化" in record["message"] or
                         "删除" in record["message"] or
                         "密码" in record["message"],
)

# 添加审计日志处理器（记录重要操作）
logger.add(
    LOGS_DIR / "audit.log",
    rotation="200 MB",
    retention="60 days",
    compression="zip",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | AUDIT | {extra[context]} - {message}",
    enqueue=True,
    filter=lambda record: "AUDIT" in record["message"] or
                         "创建成功" in record["message"] or
                         "更新成功" in record["message"] or
                         "删除成功" in record["message"],
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

# 创建专用的日志函数
def log_security(message: str, level: str = "INFO"):
    """记录安全相关日志"""
    log_message = f"SECURITY: {message}"
    if level.upper() == "WARNING":
        logger.warning(log_message)
    elif level.upper() == "ERROR":
        logger.error(log_message)
    else:
        logger.info(log_message)

def log_audit(message: str, context: str = "system", level: str = "INFO"):
    """记录审计日志"""
    log_message = f"AUDIT: {message}"
    logger.bind(context=context).info(log_message)

def log_operation(message: str, level: str = "INFO"):
    """记录一般操作日志"""
    if level.upper() == "DEBUG":
        logger.debug(message)
    elif level.upper() == "WARNING":
        logger.warning(message)
    elif level.upper() == "ERROR":
        logger.error(message)
    else:
        logger.info(message)
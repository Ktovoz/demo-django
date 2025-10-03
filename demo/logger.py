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

def get_client_info(request):
    """
    获取客户端信息（IP地址和浏览器标识）
    
    Args:
        request: Django请求对象
        
    Returns:
        dict: 包含IP地址和浏览器标识的字典
    """
    # 获取真实IP地址（考虑代理情况）
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', 'unknown')
    
    # 获取浏览器标识
    user_agent = request.META.get('HTTP_USER_AGENT', 'unknown')
    
    return {
        'ip': ip,
        'user_agent': user_agent
    }

def format_client_info(client_info):
    """
    格式化客户端信息用于日志记录
    
    Args:
        client_info (dict): 客户端信息字典
        
    Returns:
        str: 格式化后的字符串
    """
    ip = client_info.get('ip', 'unknown')
    user_agent = client_info.get('user_agent', 'unknown')
    
    # 简化浏览器标识，只保留关键信息
    if user_agent != 'unknown':
        # 提取浏览器名称和版本
        if 'Chrome' in user_agent and 'Edg' in user_agent:
            browser = 'Edge'
        elif 'Chrome' in user_agent:
            browser = 'Chrome'
        elif 'Firefox' in user_agent:
            browser = 'Firefox'
        elif 'Safari' in user_agent:
            browser = 'Safari'
        elif 'Edge' in user_agent:
            browser = 'Edge'
        else:
            browser = 'Other'
        
        # 提取操作系统信息
        if 'Windows' in user_agent:
            os_info = 'Windows'
        elif 'Mac' in user_agent:
            os_info = 'Mac'
        elif 'Linux' in user_agent:
            os_info = 'Linux'
        elif 'Android' in user_agent:
            os_info = 'Android'
        elif 'iPhone' in user_agent or 'iPad' in user_agent:
            os_info = 'iOS'
        else:
            os_info = 'Other'
        
        user_agent_info = f"{browser}/{os_info}"
    else:
        user_agent_info = 'unknown'
    
    return f"[IP:{ip}|Browser:{user_agent_info}]"

# 创建专用的日志函数
def log_security(message: str, request=None, level: str = "INFO"):
    """记录安全相关日志"""
    if request:
        client_info = get_client_info(request)
        client_info_str = format_client_info(client_info)
        log_message = f"SECURITY: {client_info_str} {message}"
    else:
        log_message = f"SECURITY: {message}"
    
    if level.upper() == "WARNING":
        logger.warning(log_message)
    elif level.upper() == "ERROR":
        logger.error(log_message)
    else:
        logger.info(log_message)

def log_audit(message: str, request=None, context: str = "system", level: str = "INFO"):
    """记录审计日志"""
    if request:
        client_info = get_client_info(request)
        client_info_str = format_client_info(client_info)
        log_message = f"AUDIT: {client_info_str} {message}"
    else:
        log_message = f"AUDIT: {message}"
    
    logger.bind(context=context).info(log_message)

def log_operation(message: str, request=None, level: str = "INFO"):
    """记录一般操作日志"""
    if request:
        client_info = get_client_info(request)
        client_info_str = format_client_info(client_info)
        log_message = f"{client_info_str} {message}"
    else:
        log_message = message
    
    if level.upper() == "DEBUG":
        logger.debug(log_message)
    elif level.upper() == "WARNING":
        logger.warning(log_message)
    elif level.upper() == "ERROR":
        logger.error(log_message)
    else:
        logger.info(log_message)
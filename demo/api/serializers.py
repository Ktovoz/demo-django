"""
数据序列化模块

提供数据序列化功能，将Django模型对象转换为JSON可序列化的字典格式。
"""

def serialize_user(user):
    """
    序列化用户对象为字典格式
    
    参数:
        user (User): Django User模型实例
    
    返回:
        dict: 包含用户信息的字典
            - id (int): 用户ID
            - username (str): 用户名
            - email (str): 邮箱地址
            - is_active (bool): 是否激活
            - group_name (str): 所属用户组名称（如果有）
            - date_joined (str): 注册时间（ISO格式）
    """
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_active': user.is_active,
        'group_name': user.groups.first().name if user.groups.exists() else None,
        'date_joined': user.date_joined.isoformat() if user.date_joined else None,
    }


def serialize_group(group):
    """
    序列化用户组对象为字典格式
    
    参数:
        group (Group): Django Group模型实例
    
    返回:
        dict: 包含用户组信息的字典
            - id (int): 用户组ID
            - name (str): 用户组名称
            - user_count (int): 用户组中的用户数量
    """
    return {
        'id': group.id,
        'name': group.name,
        'user_count': group.user_set.count(),
    }


def serialize_user_list(users):
    """
    序列化用户列表
    
    参数:
        users (QuerySet or list): 用户对象列表或查询集
    
    返回:
        list: 用户信息字典列表
    """
    return [serialize_user(user) for user in users]


def serialize_group_list(groups):
    """
    序列化用户组列表
    
    参数:
        groups (QuerySet or list): 用户组对象列表或查询集
    
    返回:
        list: 用户组信息字典列表
    """
    return [serialize_group(group) for group in groups]
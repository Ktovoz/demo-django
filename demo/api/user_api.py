"""
用户管理API模块

提供用户相关的RESTful API接口，包括用户创建、更新、删除、密码修改等功能。
所有API都需要相应的权限验证。
"""

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, Group
import json

# 导入日志模块
from ..logger import logger, log_operation, log_audit, log_security


@login_required(login_url='demo:login')
@permission_required('auth.add_user', login_url='demo:login')
@require_http_methods(["POST"])
def user_create(request):
    """
    创建新用户API
    
    需要权限: auth.add_user
    请求方法: POST
    请求参数:
        - username (str): 用户名
        - email (str, 可选): 邮箱地址
        - password (str): 密码
        - group_id (int, 可选): 用户组ID
        - is_active (bool, 可选): 是否激活，默认为True
    
    返回:
        - 成功: {'status': 'success', 'message': '用户创建成功'}
        - 失败: {'status': 'error', 'message': 错误信息}
    
    错误情况:
        - 用户名已存在 (400)
        - 密码为空 (400)
        - 其他异常 (500)
    """
    try:
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        group_id = data.get('group_id')
        is_active = data.get('is_active', True)
        log_operation(f"管理员 {request.user.username} 尝试创建用户: {username}", request)
        
        # 检查用户名是否已存在
        if User.objects.filter(username=username).exists():
            log_operation(f"用户创建失败: {username} - 用户名已存在", request)
            return JsonResponse({'status': 'error', 'message': '用户名已存在'}, status=400)
        
        # 检查密码是否为空
        password = data.get('password')
        if not password:
            log_operation(f"用户创建失败: {username} - 创建用户时密码不能为空", request)
            return JsonResponse({'status': 'error', 'message': '创建用户时密码不能为空'}, status=400)
        
        # 创建用户
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.is_active = is_active
        
        # 添加到指定用户组
        if group_id:
            group = Group.objects.get(pk=group_id)
            user.groups.add(group)
        
        user.save()
        log_audit(f"用户创建成功: {username}", request, context="user_management")
        return JsonResponse({'status': 'success', 'message': '用户创建成功'})
    except Exception as e:
        log_operation(f"用户创建失败: {username} - {str(e)}", request, level="ERROR")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@login_required(login_url='demo:login')
@permission_required('auth.change_user', login_url='demo:login')
@require_http_methods(["POST"])
def user_update(request, user_id):
    """
    更新用户信息API
    
    需要权限: auth.change_user
    请求方法: POST
    URL参数:
        - user_id (int): 用户ID
    请求参数:
        - username (str): 新用户名
        - email (str, 可选): 新邮箱地址
        - password (str, 可选): 新密码（如果提供则修改密码）
        - group_id (int, 可选): 新用户组ID
        - is_active (bool, 可选): 是否激活
    
    返回:
        - 成功: {'status': 'success', 'message': '用户信息更新成功'}
        - 失败: {'status': 'error', 'message': 错误信息}
    
    错误情况:
        - 用户名已存在 (400)
        - 其他异常 (500)
    """
    try:
        data = json.loads(request.body)
        user = get_object_or_404(User, pk=user_id)
        
        username = data.get('username')
        log_operation(f"管理员 {request.user.username} 尝试更新用户信息: {user.username} -> {username}", request)
        
        # 检查新用户名是否已存在（排除当前用户）
        if User.objects.exclude(pk=user_id).filter(username=username).exists():
            log_operation(f"用户信息更新失败: {username} - 用户名已存在", request)
            return JsonResponse({'status': 'error', 'message': '用户名已存在'}, status=400)
        
        # 更新基本信息
        user.username = username
        user.email = data.get('email', '')
        user.is_active = data.get('is_active', True)
        
        # 如果提供了新密码，则更新密码
        password = data.get('password')
        if password:
            user.set_password(password)
            log_security(f"用户密码已更新: {username}", request)
        
        # 更新用户组
        group_id = data.get('group_id')
        user.groups.clear()
        if group_id:
            group = Group.objects.get(pk=group_id)
            user.groups.add(group)
            log_operation(f"用户组已更新: {username} -> {group.name}", request)
        
        user.save()
        log_audit(f"用户信息更新成功: {username}", request, context="user_management")
        return JsonResponse({'status': 'success', 'message': '用户信息更新成功'})
    except Exception as e:
        log_operation(f"用户信息更新失败: {username} - {str(e)}", request, level="ERROR")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@login_required(login_url='demo:login')
@permission_required('auth.delete_user', login_url='demo:login')
@require_http_methods(["POST"])
def user_delete(request, user_id):
    """
    删除用户API
    
    需要权限: auth.delete_user
    请求方法: POST
    URL参数:
        - user_id (int): 要删除的用户ID
    
    返回:
        - 成功: {'status': 'success', 'message': '用户删除成功'}
        - 失败: {'status': 'error', 'message': 错误信息}
    
    错误情况:
        - 不能删除当前登录用户 (400)
        - 其他异常 (500)
    """
    # 防止用户删除自己
    if request.user.id == int(user_id):
        log_operation(f"用户删除失败: {request.user.username} 尝试删除自己", request)
        return JsonResponse({'status': 'error', 'message': '不能删除当前登录用户'}, status=400)
    
    try:
        user = get_object_or_404(User, pk=user_id)
        username = user.username
        log_operation(f"管理员 {request.user.username} 尝试删除用户: {username}", request)
        user.delete()
        log_audit(f"用户删除成功: {username}", request, context="user_management")
        return JsonResponse({'status': 'success', 'message': '用户删除成功'})
    except Exception as e:
        log_operation(f"用户删除失败: {username} - {str(e)}", request, level="ERROR")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@login_required(login_url='demo:login')
@permission_required('auth.change_user', login_url='demo:login')
@require_http_methods(["POST"])
def change_user_group(request, user_id):
    """
    修改用户组API
    
    需要权限: auth.change_user
    请求方法: POST
    URL参数:
        - user_id (int): 用户ID
    请求参数:
        - group_id (int, 可选): 新用户组ID，如果为空则移除用户组
    
    返回:
        - 成功: {'status': 'success', 'message': '用户组更新成功'}
        - 失败: {'status': 'error', 'message': 错误信息}
    
    权限限制:
        - 普通管理员只能管理普通用户
        - 不能修改自己的用户组
    """
    try:
        data = json.loads(request.body)
        user = get_object_or_404(User, pk=user_id)
        current_user = request.user
        
        # 权限检查：非超级管理员只能管理普通用户
        if not current_user.groups.filter(name='超级管理员').exists():
            user_group = Group.objects.get(name='普通用户')
            if not user.groups.filter(id=user_group.id).exists():
                log_operation(f"用户组更新失败: {current_user.username} 尝试管理非普通用户 {user.username}", request)
                return JsonResponse({
                    'status': 'error',
                    'message': '您只能管理普通用户'
                }, status=403)

        # 防止用户修改自己的用户组
        if user.id == current_user.id:
            log_operation(f"用户组更新失败: {user.username} 尝试修改自己的用户组", request)
            return JsonResponse({
                'status': 'error',
                'message': '不能修改自己的用户组'
            }, status=400)

        # 记录原用户组
        old_groups = list(user.groups.values_list('name', flat=True))

        # 更新用户组
        user.groups.clear()
        group_id = data.get('group_id')
        if group_id:
            group = Group.objects.get(pk=group_id)
            user.groups.add(group)
            new_group_name = group.name
        else:
            new_group_name = "无组"

        log_operation(f"用户组更新成功: {user.username} {old_groups} -> {new_group_name}", request)
        log_audit(f"用户组变更: {user.username} {old_groups} -> {new_group_name}", request, context="user_management")
        return JsonResponse({
            'status': 'success',
            'message': '用户组更新成功'
        })
    except Exception as e:
        log_operation(f"用户组更新失败: {user.username if 'user' in locals() else 'unknown'} - {str(e)}", request, level="ERROR")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@login_required
@require_http_methods(["POST"])
def change_password(request, user_id):
    """
    修改用户密码API
    
    请求方法: POST
    URL参数:
        - user_id (int): 用户ID
    请求参数:
        - new_password (str): 新密码
    
    返回:
        - 成功: {'status': 'success', 'message': '密码修改成功'}
        - 失败: {'status': 'error', 'message': 错误信息}
    
    权限说明:
        - 超级管理员可以修改任意用户密码
        - 普通用户只能修改自己的密码
    """
    # 权限检查：非超级管理员且不是用户自己则拒绝
    if not request.user.is_superuser and request.user.id != user_id:
        log_operation(f"密码修改失败: {request.user.username} 尝试修改用户 {user_id} 的密码但没有权限", request)
        return JsonResponse({'status': 'error', 'message': '没有权限'}, status=403)
    
    try:
        data = json.loads(request.body)
        user = get_object_or_404(User, pk=user_id)
        log_operation(f"用户 {request.user.username} 尝试修改密码: {user.username}", request)
        
        # 检查新密码是否为空
        new_password = data.get('new_password')
        if not new_password:
            log_operation(f"密码修改失败: {user.username} - 新密码不能为空", request)
            return JsonResponse({'status': 'error', 'message': '新密码不能为空'}, status=400)
        
        # 修改密码
        user.set_password(new_password)
        user.save()
        log_security(f"密码修改成功: {user.username}", request)
        log_audit(f"用户密码变更: {user.username}", request, context="user_management")
        return JsonResponse({'status': 'success', 'message': '密码修改成功'})
    except Exception as e:
        log_operation(f"密码修改失败: {user.username} - {str(e)}", request, level="ERROR")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@login_required(login_url='demo:login')
@permission_required('auth.change_user', login_url='demo:login')
def available_users_for_group(request, group_id):
    """
    获取可添加到指定用户组的用户列表API
    
    需要权限: auth.change_user
    请求方法: GET
    URL参数:
        - group_id (int): 用户组ID
    
    返回:
        JSON格式的用户列表:
        {
            'users': [
                {
                    'id': 用户ID,
                    'username': 用户名
                },
                ...
            ]
        }
    
    说明:
        - 返回未属于指定用户组的用户
        - 普通管理员只能看到普通用户
        - 超级管理员可以看到所有用户
    """
    group = get_object_or_404(Group, pk=group_id)
    current_user = request.user

    # 获取不在此用户组中的用户
    available_users = User.objects.exclude(groups=group)
    log_operation(f"查询可分配到用户组 '{group.name}' 的用户", request)

    # 权限限制：非超级管理员只能看到普通用户
    if not current_user.groups.filter(name='超级管理员').exists():
        user_group = Group.objects.get(name='普通用户')
        available_users = available_users.filter(groups=user_group)
        log_operation(f"管理员 {current_user.username} 只能管理普通用户", request)

    user_count = available_users.count()
    log_operation(f"用户组 '{group.name}' 可分配用户数量: {user_count}", request)

    return JsonResponse({
        'users': [
            {
                'id': user.id,
                'username': user.username
            }
            for user in available_users
        ]
    })
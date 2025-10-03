"""
用户组管理API模块

提供用户组相关的RESTful API接口，包括用户组创建、更新等功能。
所有API都需要相应的权限验证。
"""

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
import json

# 导入日志模块
from ..logger import logger


@login_required(login_url='demo:login')
@permission_required('auth.add_group', login_url='demo:login')
@require_http_methods(["POST"])
def group_create(request):
    """
    创建新用户组API
    
    需要权限: auth.add_group
    请求方法: POST
    请求参数:
        - name (str): 用户组名称
    
    返回:
        - 成功: {'status': 'success', 'message': '用户组创建成功'}
        - 失败: {'status': 'error', 'message': 错误信息}
    
    错误情况:
        - 用户组名已存在 (400)
        - 其他异常 (500)
    """
    try:
        data = json.loads(request.body)
        name = data.get('name')
        logger.info(f"管理员 {request.user.username} 尝试创建用户组: {name}")
        
        # 检查用户组名是否已存在
        if Group.objects.filter(name=name).exists():
            logger.warning(f"用户组创建失败: {name} - 用户组名已存在")
            return JsonResponse({'status': 'error', 'message': '用户组名已存在'}, status=400)
        
        # 创建用户组
        group = Group.objects.create(name=name)
        logger.info(f"用户组创建成功: {name}")
        return JsonResponse({'status': 'success', 'message': '用户组创建成功'})
    except Exception as e:
        logger.error(f"用户组创建失败: {name} - {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@login_required(login_url='demo:login')
@permission_required('auth.change_group', login_url='demo:login')
@require_http_methods(["POST"])
def group_update(request, group_id):
    """
    更新用户组信息API
    
    需要权限: auth.change_group
    请求方法: POST
    URL参数:
        - group_id (int): 用户组ID
    请求参数:
        - name (str): 新用户组名称
    
    返回:
        - 成功: {'status': 'success', 'message': '用户组更新成功'}
        - 失败: {'status': 'error', 'message': 错误信息}
    
    错误情况:
        - 用户组名已存在 (400)
        - 其他异常 (500)
    """
    try:
        data = json.loads(request.body)
        group = get_object_or_404(Group, pk=group_id)
        old_name = group.name
        name = data.get('name')
        logger.info(f"管理员 {request.user.username} 尝试更新用户组: {old_name} -> {name}")
        
        # 检查新用户组名是否已存在（排除当前用户组）
        if Group.objects.exclude(pk=group_id).filter(name=name).exists():
            logger.warning(f"用户组更新失败: {name} - 用户组名已存在")
            return JsonResponse({'status': 'error', 'message': '用户组名已存在'}, status=400)
        
        # 更新用户组名称
        group.name = name
        group.save()
        logger.info(f"用户组更新成功: {old_name} -> {name}")
        return JsonResponse({'status': 'success', 'message': '用户组更新成功'})
    except Exception as e:
        logger.error(f"用户组更新失败: {name} - {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
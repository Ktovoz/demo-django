from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json

# 导入日志模块
from ..logger import logger


@login_required(login_url='demo:login')
@permission_required('auth.view_group', login_url='demo:login')
def group_list(request):
    logger.info(f"管理员 {request.user.username} 访问用户组列表页面")
    groups = Group.objects.all()
    group_count = groups.count()
    logger.debug(f"当前用户组总数: {group_count}")
    for group in groups:
        member_count = group.user_set.count()
        logger.debug(f"用户组 '{group.name}' 成员数量: {member_count}")
    context = {
        'groups': groups,
        'title': '用户组管理'
    }
    return render(request, 'demo/group_list.html', context)


@login_required(login_url='demo:login')
@permission_required('auth.view_group', login_url='demo:login')
def group_detail_api(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    user_count = group.user_set.count()
    logger.info(f"管理员 {request.user.username} 查看用户组详情: {group.name}")
    logger.debug(f"用户组 '{group.name}' 成员数量: {user_count}")
    return JsonResponse({
        'name': group.name,
        'user_count': user_count
    })


@login_required(login_url='demo:login')
@permission_required('auth.view_group', login_url='demo:login')
def group_members(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    members = group.user_set.all()
    member_count = members.count()
    active_count = members.filter(is_active=True).count()
    logger.info(f"管理员 {request.user.username} 查看用户组成员: {group.name}")
    logger.debug(f"用户组 '{group.name}' 成员统计: 总数 {member_count}, 激活 {active_count}")
    return JsonResponse({
        'group_name': group.name,
        'members': [
            {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_active': user.is_active
            }
            for user in members
        ]
    })
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json

# 导入日志模块
from ..logger import logger


@login_required(login_url='demo:login')
@permission_required('auth.view_user', login_url='demo:login')
def user_list(request):
    logger.info(f"管理员 {request.user.username} 访问用户列表页面")
    users = User.objects.all()
    groups = Group.objects.all()
    user_count = users.count()
    group_count = groups.count()
    logger.debug(f"当前用户总数: {user_count}, 用户组总数: {group_count}")
    context = {
        'users': users,
        'groups': groups,
        'title': '用户管理'
    }
    return render(request, 'demo/user_list.html', context)


@login_required(login_url='demo:login')
@permission_required('auth.view_user', login_url='demo:login')
def user_detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    logger.info(f"管理员 {request.user.username} 查看用户详情: {user.username}")
    logger.debug(f"用户 {user.username} 信息 - 邮箱: {user.email}, 状态: {'激活' if user.is_active else '未激活'}")
    context = {
        'user_detail': user,
        'groups': Group.objects.all(),
        'title': '用户详情'
    }
    return render(request, 'demo/user_detail.html', context)


@login_required(login_url='demo:login')
@permission_required('auth.view_user', login_url='demo:login')
def users_api(request):
    logger.info(f"管理员 {request.user.username} 请求用户数据API")
    users = User.objects.all()
    user_count = users.count()
    active_count = users.filter(is_active=True).count()
    logger.debug(f"返回用户数据: 总数 {user_count}, 激活 {active_count}")
    return JsonResponse({
        'users': [
            {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'group_name': user.groups.first().name if user.groups.exists() else None,
                'is_active': user.is_active
            }
            for user in users
        ]
    })
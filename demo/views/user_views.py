from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json

# 导入日志模块
from ..logger import logger, log_operation, log_audit


@login_required(login_url='demo:login')
@permission_required('auth.view_user', login_url='demo:login')
def user_list(request):
    log_operation(f"管理员 {request.user.username} 访问用户列表页面", request)
    users = User.objects.all()
    groups = Group.objects.all()
    user_count = users.count()
    group_count = groups.count()
    log_operation(f"当前用户总数: {user_count}, 用户组总数: {group_count}", request)
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
    log_operation(f"Admin {request.user.username} viewed user detail: {user.username}", request)
    log_operation(f"User {user.username} snapshot - email: {user.email or 'N/A'}, status: {'ACTIVE' if user.is_active else 'INACTIVE'}", request)

    primary_group = user.groups.first()
    payload = {
        'status': 'success',
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'full_name': user.get_full_name(),
        'group_id': primary_group.id if primary_group else None,
        'group_name': primary_group.name if primary_group else None,
        'is_active': user.is_active,
        'date_joined': user.date_joined.isoformat(),
        'last_login': user.last_login.isoformat() if user.last_login else None
    }

    accept_header = request.headers.get('Accept', '')
    wants_json = request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in accept_header or request.GET.get('format') == 'json'

    if wants_json:
        return JsonResponse(payload)

    context = {
        'user_detail': user,
        'groups': Group.objects.all(),
        'title': '用户详情'
    }
    return render(request, 'demo/user_detail.html', context)
def users_api(request):
    log_operation(f"管理员 {request.user.username} 请求用户数据API", request)
    users = User.objects.all()
    user_count = users.count()
    active_count = users.filter(is_active=True).count()
    log_operation(f"返回用户数据: 总数 {user_count}, 激活 {active_count}", request)
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

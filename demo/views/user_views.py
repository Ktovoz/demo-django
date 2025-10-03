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
    users = User.objects.all()
    groups = Group.objects.all()
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
    context = {
        'user_detail': user,
        'groups': Group.objects.all(),
        'title': '用户详情'
    }
    return render(request, 'demo/user_detail.html', context)


@login_required(login_url='demo:login')
@permission_required('auth.view_user', login_url='demo:login')
def users_api(request):
    users = User.objects.all()
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
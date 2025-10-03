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
    groups = Group.objects.all()
    context = {
        'groups': groups,
        'title': '用户组管理'
    }
    return render(request, 'demo/group_list.html', context)


@login_required(login_url='demo:login')
@permission_required('auth.view_group', login_url='demo:login')
def group_detail_api(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    return JsonResponse({
        'name': group.name,
        'user_count': group.user_set.count()
    })


@login_required(login_url='demo:login')
@permission_required('auth.view_group', login_url='demo:login')
def group_members(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    members = group.user_set.all()
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
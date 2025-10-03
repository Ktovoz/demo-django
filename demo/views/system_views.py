from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
import json

# 导入日志模块
from ..logger import logger


@require_http_methods(["GET"])
def init_system(request, password):
    init_password = 'admin123'  

    if password != init_password:
        return JsonResponse({'status': 'error', 'message': '初始化密码错误'}, status=403)

    try:
        # 清理现有数据
        try:
            User.objects.all().delete()
            Group.objects.all().delete()
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'清理现有数据失败：{str(e)}'}, status=500)

        # 创建用户组
        try:
            superadmin_group = Group.objects.create(name='超级管理员')
            admin_group = Group.objects.create(name='管理员')
            user_group = Group.objects.create(name='普通用户')
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'创建用户组失败：{str(e)}'}, status=500)

        # 设置权限
        try:
            user_ct = ContentType.objects.get_for_model(User)
            group_ct = ContentType.objects.get_for_model(Group)
            user_permissions = Permission.objects.filter(content_type=user_ct)
            group_permissions = Permission.objects.filter(content_type=group_ct)
            
            # 超级管理员权限
            superadmin_group.permissions.set(list(user_permissions) + list(group_permissions))
            
            # 管理员权限
            admin_user_permissions = Permission.objects.filter(
                content_type__in=[user_ct, group_ct],
                codename__in=['add_user', 'change_user', 'delete_user', 'view_user', 'view_group']
            )
            admin_group.permissions.set(admin_user_permissions)
            
            # 普通用户权限
            user_view_permissions = Permission.objects.filter(
                content_type__in=[user_ct, group_ct],
                codename__in=['view_user', 'view_group']
            )
            user_group.permissions.set(user_view_permissions)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'设置权限失败：{str(e)}'}, status=500)

        # 创建超级管理员用户
        try:
            admin_user = User.objects.create_superuser(
                username='admin',
                password='admin',
                email='admin@example.com'
            )
            admin_user.groups.add(superadmin_group)
            admin_user.save()
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'创建管理员用户失败：{str(e)}'}, status=500)
        
        return JsonResponse({
            'status': 'success', 
            'message': '系统初始化成功',
            'data': {
                'admin_username': 'admin',
                'admin_password': 'admin'
            }
        })
    except Exception as e:
        # 发生未知错误时，尝试清理所有数据
        try:
            User.objects.all().delete()
            Group.objects.all().delete()
            return JsonResponse({
                'status': 'error', 
                'message': f'初始化过程中发生未知错误，已清理数据。错误信息：{str(e)}'
            }, status=500)
        except Exception as cleanup_error:
            return JsonResponse({
                'status': 'error', 
                'message': f'初始化和清理均失败。错误信息：{str(cleanup_error)}'
            }, status=500)
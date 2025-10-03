from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission
from django.shortcuts import get_object_or_404
import json

# 导入日志模块
from ..logger import logger, log_operation, log_audit, log_security


@require_http_methods(["GET"])
def init_system(request, password):
    """
    系统初始化API

    功能：
    1. 清理现有用户和用户组数据
    2. 创建默认用户组（超级管理员、管理员、普通用户）
    3. 设置用户组权限
    4. 创建默认管理员账户

    安全警告：此操作会删除所有现有数据，请谨慎使用
    """
    init_password = 'admin123'
    client_ip = request.META.get('REMOTE_ADDR', 'unknown')

    log_security(f"系统初始化请求 - IP: {client_ip}, 密码: {password}", request)

    if password != init_password:
        log_security(f"系统初始化失败 - 密码错误，IP: {client_ip}", request)
        return JsonResponse({'status': 'error', 'message': '初始化密码错误'}, status=403)

    try:
        log_operation("开始系统初始化...", request)

        # 1. 清理现有数据
        try:
            user_count = User.objects.count()
            group_count = Group.objects.count()
            log_operation(f"清理现有数据 - 用户: {user_count}, 用户组: {group_count}", request)

            User.objects.all().delete()
            Group.objects.all().delete()
            log_operation("现有数据清理完成", request)
        except Exception as e:
            log_operation(f"清理现有数据失败: {str(e)}", request, level="ERROR")
            return JsonResponse({'status': 'error', 'message': f'清理现有数据失败：{str(e)}'}, status=500)

        # 2. 创建用户组
        try:
            log_operation("开始创建默认用户组...", request)
            superadmin_group = Group.objects.create(name='超级管理员')
            admin_group = Group.objects.create(name='管理员')
            user_group = Group.objects.create(name='普通用户')
            log_operation("用户组创建完成: 超级管理员, 管理员, 普通用户", request)
        except Exception as e:
            log_operation(f"创建用户组失败: {str(e)}", request, level="ERROR")
            return JsonResponse({'status': 'error', 'message': f'创建用户组失败：{str(e)}'}, status=500)

        # 3. 设置权限
        try:
            log_operation("开始设置用户组权限...", request)
            user_ct = ContentType.objects.get_for_model(User)
            group_ct = ContentType.objects.get_for_model(Group)
            user_permissions = Permission.objects.filter(content_type=user_ct)
            group_permissions = Permission.objects.filter(content_type=group_ct)

            # 超级管理员权限 - 所有权限
            superadmin_group.permissions.set(list(user_permissions) + list(group_permissions))
            log_operation(f"超级管理员权限设置完成 - 用户权限: {user_permissions.count()}, 组权限: {group_permissions.count()}", request)

            # 管理员权限 - 有限的用户管理权限
            admin_user_permissions = Permission.objects.filter(
                content_type__in=[user_ct, group_ct],
                codename__in=['add_user', 'change_user', 'delete_user', 'view_user', 'view_group']
            )
            admin_group.permissions.set(admin_user_permissions)
            log_operation(f"管理员权限设置完成 - 权限数量: {admin_user_permissions.count()}", request)

            # 普通用户权限 - 只读权限
            user_view_permissions = Permission.objects.filter(
                content_type__in=[user_ct, group_ct],
                codename__in=['view_user', 'view_group']
            )
            user_group.permissions.set(user_view_permissions)
            log_operation(f"普通用户权限设置完成 - 权限数量: {user_view_permissions.count()}", request)

            log_operation("用户组权限设置完成", request)
        except Exception as e:
            log_operation(f"设置权限失败: {str(e)}", request, level="ERROR")
            return JsonResponse({'status': 'error', 'message': f'设置权限失败：{str(e)}'}, status=500)

        # 4. 创建超级管理员用户
        try:
            log_operation("开始创建超级管理员用户...", request)
            admin_user = User.objects.create_superuser(
                username='admin',
                password='admin',
                email='admin@example.com'
            )
            admin_user.groups.add(superadmin_group)
            admin_user.save()
            log_operation("超级管理员用户创建完成 - 用户名: admin, 邮箱: admin@example.com", request)
        except Exception as e:
            log_operation(f"创建管理员用户失败: {str(e)}", request, level="ERROR")
            return JsonResponse({'status': 'error', 'message': f'创建管理员用户失败：{str(e)}'}, status=500)

        log_audit("系统初始化完成！", request, context="system")
        return JsonResponse({
            'status': 'success',
            'message': '系统初始化成功',
            'data': {
                'admin_username': 'admin',
                'admin_password': 'admin'
            }
        })
    except Exception as e:
        log_operation(f"系统初始化发生未知错误: {str(e)}", request, level="ERROR")
        # 发生未知错误时，尝试清理所有数据
        try:
            log_operation("尝试清理初始化过程中的数据...", request)
            User.objects.all().delete()
            Group.objects.all().delete()
            log_operation("数据清理完成", request)
            return JsonResponse({
                'status': 'error',
                'message': f'初始化过程中发生未知错误，已清理数据。错误信息：{str(e)}'
            }, status=500)
        except Exception as cleanup_error:
            log_operation(f"初始化和清理均失败: {str(cleanup_error)}", request, level="CRITICAL")
            return JsonResponse({
                'status': 'error',
                'message': f'初始化和清理均失败。错误信息：{str(cleanup_error)}'
            }, status=500)


@require_http_methods(["GET"])
def test_logging(request):
    """
    测试日志记录功能
    
    用于测试新的日志记录功能，包括IP地址和浏览器标识的记录
    """
    log_operation("测试日志记录功能", request)
    log_security("测试安全日志记录", request)
    log_audit("测试审计日志记录", request, context="testing")
    
    return JsonResponse({
        'status': 'success',
        'message': '日志记录测试完成'
    })
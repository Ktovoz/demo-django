from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.models import User, Group, Permission
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import permission_required
import json
from django.contrib.contenttypes.models import ContentType


@login_required(login_url='demo:login')
def home(request):
    context = {
        'title': '用户管理',
        'current_time': timezone.now(),
        'users': User.objects.all(),
        'groups': Group.objects.all()
    }
    return render(request, 'demo/home.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('demo:home')
        else:
            messages.error(request, '用户名或密码错误')
            return render(request, 'demo/login.html', {'title': '用户登录'})
    
    return render(request, 'demo/login.html', {'title': '用户登录'})

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, '两次输入的密码不一致')
            return render(request, 'demo/register.html', {'title': '用户注册'})

        if User.objects.filter(username=username).exists():
            messages.error(request, '用户名已存在')
            return render(request, 'demo/register.html', {'title': '用户注册'})

        try:
            user = User.objects.create_user(username=username, password=password1)
    
            user_group = Group.objects.get(name='普通用户')
            user.groups.add(user_group)
            user.save()
            
            login(request, user)
            return redirect('demo:home')
        except Exception as e:
            messages.error(request, '注册失败，请稍后重试')
            return render(request, 'demo/register.html', {'title': '用户注册'})

    return render(request, 'demo/register.html', {'title': '用户注册'})

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
def user_detail_api(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return JsonResponse({
        'username': user.username,
        'email': user.email,
        'is_active': user.is_active,
        'group_id': user.groups.first().id if user.groups.exists() else None
    })

@login_required(login_url='demo:login')
@permission_required('auth.add_user', login_url='demo:login')
@require_http_methods(["POST"])
def user_create(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        group_id = data.get('group_id')
        is_active = data.get('is_active', True)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'status': 'error', 'message': '用户名已存在'}, status=400)
        
 
        password = data.get('password')
        if not password:
            return JsonResponse({'status': 'error', 'message': '创建用户时密码不能为空'}, status=400)
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.is_active = is_active
        
        if group_id:
            group = Group.objects.get(pk=group_id)
            user.groups.add(group)
        
        user.save()
        return JsonResponse({'status': 'success', 'message': '用户创建成功'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required(login_url='demo:login')
@permission_required('auth.change_user', login_url='demo:login')
@require_http_methods(["POST"])
def user_update(request, user_id):
    try:
        data = json.loads(request.body)
        user = get_object_or_404(User, pk=user_id)
        
        username = data.get('username')
        if User.objects.exclude(pk=user_id).filter(username=username).exists():
            return JsonResponse({'status': 'error', 'message': '用户名已存在'}, status=400)
        
        user.username = username
        user.email = data.get('email', '')
        user.is_active = data.get('is_active', True)
        
  
        password = data.get('password')
        if password:
            user.set_password(password)
        
        group_id = data.get('group_id')
        user.groups.clear()
        if group_id:
            group = Group.objects.get(pk=group_id)
            user.groups.add(group)
        
        user.save()
        return JsonResponse({'status': 'success', 'message': '用户信息更新成功'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required(login_url='demo:login')
@permission_required('auth.delete_user', login_url='demo:login')
@require_http_methods(["POST"])
def user_delete(request, user_id):
    if request.user.id == int(user_id):
        return JsonResponse({'status': 'error', 'message': '不能删除当前登录用户'}, status=400)
    
    try:
        user = get_object_or_404(User, pk=user_id)
        user.delete()
        return JsonResponse({'status': 'success', 'message': '用户删除成功'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

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

@login_required(login_url='demo:login')
@permission_required('auth.add_group', login_url='demo:login')
@require_http_methods(["POST"])
def group_create(request):
    try:
        data = json.loads(request.body)
        name = data.get('name')
        
        if Group.objects.filter(name=name).exists():
            return JsonResponse({'status': 'error', 'message': '用户组名已存在'}, status=400)
        
        group = Group.objects.create(name=name)
        return JsonResponse({'status': 'success', 'message': '用户组创建成功'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required(login_url='demo:login')
@permission_required('auth.change_group', login_url='demo:login')
@require_http_methods(["POST"])
def group_update(request, group_id):
    try:
        data = json.loads(request.body)
        group = get_object_or_404(Group, pk=group_id)
        
        name = data.get('name')
        if Group.objects.exclude(pk=group_id).filter(name=name).exists():
            return JsonResponse({'status': 'error', 'message': '用户组名已存在'}, status=400)
        
        group.name = name
        group.save()
        return JsonResponse({'status': 'success', 'message': '用户组更新成功'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required(login_url='demo:login')
@permission_required('auth.change_user', login_url='demo:login')
def available_users_for_group(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    current_user = request.user
    

    available_users = User.objects.exclude(groups=group)
    

    if not current_user.groups.filter(name='超级管理员').exists():
        user_group = Group.objects.get(name='普通用户')
        available_users = available_users.filter(groups=user_group)
    
    return JsonResponse({
        'users': [
            {
                'id': user.id,
                'username': user.username
            }
            for user in available_users
        ]
    })

@login_required(login_url='demo:login')
@permission_required('auth.change_user', login_url='demo:login')
@require_http_methods(["POST"])
def change_user_group(request, user_id):
    try:
        data = json.loads(request.body)
        user = get_object_or_404(User, pk=user_id)
        current_user = request.user
        
   
        if not current_user.groups.filter(name='超级管理员').exists():

            user_group = Group.objects.get(name='普通用户')
            if not user.groups.filter(id=user_group.id).exists():
                return JsonResponse({
                    'status': 'error',
                    'message': '您只能管理普通用户'
                }, status=403)
        
   
        if user.id == current_user.id:
            return JsonResponse({
                'status': 'error',
                'message': '不能修改自己的用户组'
            }, status=400)
        
      
        user.groups.clear()
        group_id = data.get('group_id')
        if group_id:
            group = Group.objects.get(pk=group_id)
            user.groups.add(group)
        
        return JsonResponse({
            'status': 'success',
            'message': '用户组更新成功'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


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

# 修改密码
@login_required
@require_http_methods(["POST"])
def change_password(request, user_id):
    if not request.user.is_superuser and request.user.id != user_id:
        return JsonResponse({'status': 'error', 'message': '没有权限'}, status=403)
    
    try:
        data = json.loads(request.body)
        user = get_object_or_404(User, pk=user_id)
        
        new_password = data.get('new_password')
        if not new_password:
            return JsonResponse({'status': 'error', 'message': '新密码不能为空'}, status=400)
        
        user.set_password(new_password)
        user.save()
        return JsonResponse({'status': 'success', 'message': '密码修改成功'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

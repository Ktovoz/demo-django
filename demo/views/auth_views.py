from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.views.decorators.http import require_http_methods

# 导入日志模块
from ..logger import logger, log_security, log_operation


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me') == 'on'
        log_security(f"用户尝试登录: {username}, 记住我: {remember_me}", request)
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # 处理记住我功能
            if remember_me:
                # 设置会话过期时间为30天
                request.session.set_expiry(30 * 24 * 60 * 60)
            else:
                # 浏览器关闭时会话过期
                request.session.set_expiry(0)
            
            log_security(f"用户登录成功: {username}", request)
            return redirect('demo:home')
        else:
            log_security(f"用户登录失败: {username} - 用户名或密码错误", request)
            messages.error(request, '用户名或密码错误')
            return render(request, 'demo/login.html', {'title': '用户登录'})
    
    log_operation("显示登录页面", request)
    return render(request, 'demo/login.html', {'title': '用户登录'})


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        log_security(f"用户尝试注册: {username}", request)

        if password1 != password2:
            log_security(f"用户注册失败: {username} - 两次输入的密码不一致", request)
            messages.error(request, '两次输入的密码不一致')
            return render(request, 'demo/register.html', {'title': '用户注册'})

        if User.objects.filter(username=username).exists():
            log_security(f"用户注册失败: {username} - 用户名已存在", request)
            messages.error(request, '用户名已存在')
            return render(request, 'demo/register.html', {'title': '用户注册'})

        try:
            user = User.objects.create_user(username=username, password=password1)
    
            user_group = Group.objects.get(name='普通用户')
            user.groups.add(user_group)
            user.save()
            
            login(request, user)
            log_security(f"用户注册成功: {username}", request)
            return redirect('demo:home')
        except Exception as e:
            log_security(f"用户注册失败: {username} - {str(e)}", request)
            messages.error(request, '注册失败，请稍后重试')
            return render(request, 'demo/register.html', {'title': '用户注册'})

    log_operation("显示注册页面", request)
    return render(request, 'demo/register.html', {'title': '用户注册'})


@login_required(login_url='demo:login')
def home(request):
    log_operation(f"用户 {request.user.username} 访问首页", request)
    user_groups = list(request.user.groups.values_list('name', flat=True))
    log_operation(f"用户 {request.user.username} 所属用户组: {user_groups}", request)

    # 统计信息
    user_count = User.objects.count()
    group_count = Group.objects.count()
    active_user_count = User.objects.filter(is_active=True).count()

    log_operation(f"系统统计 - 用户总数: {user_count}, 激活用户: {active_user_count}, 用户组: {group_count}", request)

    context = {
        'title': '用户管理',
        'current_time': timezone.now(),
        'users': User.objects.all(),
        'groups': Group.objects.all(),
        'user_count': user_count,
        'active_user_count': active_user_count,
        'group_count': group_count
    }
    return render(request, 'demo/home.html', context)
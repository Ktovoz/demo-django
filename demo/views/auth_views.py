from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.views.decorators.http import require_http_methods

# 导入日志模块
from ..logger import logger


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        logger.info(f"用户尝试登录: {username}")
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            logger.info(f"用户登录成功: {username}")
            return redirect('demo:home')
        else:
            logger.warning(f"用户登录失败: {username} - 用户名或密码错误")
            messages.error(request, '用户名或密码错误')
            return render(request, 'demo/login.html', {'title': '用户登录'})
    
    logger.debug("显示登录页面")
    return render(request, 'demo/login.html', {'title': '用户登录'})


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        logger.info(f"用户尝试注册: {username}")

        if password1 != password2:
            logger.warning(f"用户注册失败: {username} - 两次输入的密码不一致")
            messages.error(request, '两次输入的密码不一致')
            return render(request, 'demo/register.html', {'title': '用户注册'})

        if User.objects.filter(username=username).exists():
            logger.warning(f"用户注册失败: {username} - 用户名已存在")
            messages.error(request, '用户名已存在')
            return render(request, 'demo/register.html', {'title': '用户注册'})

        try:
            user = User.objects.create_user(username=username, password=password1)
    
            user_group = Group.objects.get(name='普通用户')
            user.groups.add(user_group)
            user.save()
            
            login(request, user)
            logger.info(f"用户注册成功: {username}")
            return redirect('demo:home')
        except Exception as e:
            logger.error(f"用户注册失败: {username} - {str(e)}")
            messages.error(request, '注册失败，请稍后重试')
            return render(request, 'demo/register.html', {'title': '用户注册'})

    logger.debug("显示注册页面")
    return render(request, 'demo/register.html', {'title': '用户注册'})


@login_required(login_url='demo:login')
def home(request):
    logger.info(f"用户 {request.user.username} 访问首页")
    user_groups = list(request.user.groups.values_list('name', flat=True))
    logger.debug(f"用户 {request.user.username} 所属用户组: {user_groups}")

    # 统计信息
    user_count = User.objects.count()
    group_count = Group.objects.count()
    active_user_count = User.objects.filter(is_active=True).count()

    logger.debug(f"系统统计 - 用户总数: {user_count}, 激活用户: {active_user_count}, 用户组: {group_count}")

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
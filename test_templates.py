import os
import django
from django.conf import settings
from django.template.loader import get_template

# 配置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

try:
    # 测试基础模板
    template = get_template('demo/base.html')
    print("基础模板语法正确")
    
    # 测试登录模板
    template = get_template('demo/login.html')
    print("登录模板语法正确")
    
    # 测试注册模板
    template = get_template('demo/register.html')
    print("注册模板语法正确")
    
    # 测试主页模板
    template = get_template('demo/home.html')
    print("主页模板语法正确")
    
except Exception as e:
    print(f"模板语法错误: {e}")
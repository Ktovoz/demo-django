from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
from django.contrib import admin as admin_site
from django.urls import path
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.urls import reverse

# 自定义Admin站点配置
class MyAdminSite(admin.AdminSite):
    site_header = 'Django Hub 管理后台'
    site_title = 'Django Hub'
    index_title = '欢迎使用 Django Hub 管理系统'

    def each_context(self, request):
        context = super().each_context(request)
        context['custom_css'] = '/static/css/admin-style.css'
        return context

# 创建自定义管理站点
my_admin_site = MyAdminSite(name='myadmin')

# 自定义用户管理
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('个人信息', {'fields': ('first_name', 'last_name', 'email')}),
        ('权限设置', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('重要日期', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )

# 自定义用户组管理
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'member_count')
    search_fields = ('name',)
    filter_horizontal = ('permissions',)

    def member_count(self, obj):
        return obj.user_set.count()
    member_count.short_description = '成员数量'

# 注册模型到自定义管理站点
my_admin_site.register(User, UserAdmin)
my_admin_site.register(Group, GroupAdmin)

# 取消默认注册，然后使用自定义样式重新注册

# 自定义管理站点外观
admin.site.site_header = 'Django Hub 管理后台'
admin.site.site_title = 'Django Hub'
admin.site.index_title = '欢迎使用 Django Hub 管理系统'

# 添加自定义CSS到管理界面
class CustomAdminMixin:
    """自定义Admin混入类，用于添加自定义样式"""

    class Media:
        css = {
            'all': ('css/admin-style.css',)
        }
        js = ()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '请输入用户名'
        })
        form.base_fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '请输入密码'
        })
        return form

# 为所有Admin类添加自定义样式
def get_custom_admin_classes():
    """获取所有带有自定义样式的Admin类"""
    return [
        (User, UserAdmin),
        (Group, GroupAdmin),
    ]

# 注册自定义Admin类
for model, admin_class in get_custom_admin_classes():
    # 继承原有的Admin配置并添加自定义样式
    class CustomAdminClass(admin_class, CustomAdminMixin):
        pass
    CustomAdminClass.__name__ = f'Custom{admin_class.__name__}'
    admin.site.unregister(model)
    admin.site.register(model, CustomAdminClass)

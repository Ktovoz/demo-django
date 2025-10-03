# 为了向后兼容，从新模块导入所有视图函数
from .views.auth_views import login_view, register_view, home
from .views.user_views import user_list, user_detail, users_api
from .views.group_views import group_list, group_detail_api, group_members
from .views.system_views import init_system
from .api.user_api import user_create, user_update, user_delete, change_user_group, change_password, available_users_for_group, user_detail_api
from .api.group_api import group_create, group_update

# 为了保持URL路由的兼容性，需要重新导出一些函数
# user_detail_api在user_views和user_api中都存在，这里使用user_views中的版本
# 如果需要使用API版本，应该在urls.py中明确指定
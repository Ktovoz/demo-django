from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import auth_views, user_views, group_views, system_views
from .api import user_api, group_api
from django.views.generic import RedirectView

app_name = 'demo'

urlpatterns = [
    path('init/<str:password>/', system_views.init_system, name='init_system'),
    path('test-logging/', system_views.test_logging, name='test_logging'),
    
    path('', auth_views.home, name='home'),
    path('login/', auth_views.login_view, name='login'),
    path('register/', auth_views.register_view, name='register'),
    path('check-username/', auth_views.check_username, name='check_username'),
    path('logout/', LogoutView.as_view(next_page='demo:login', template_name='demo/login.html'), name='logout'),
    
    # API endpoints
    path('users/api/', user_views.users_api, name='users_api'),
    path('users/', user_views.user_list, name='user_list'),
    path('users/create/', user_api.user_create, name='user_create'),
    path('users/<int:user_id>/', user_views.user_detail, name='user_detail'),
    path('users/<int:user_id>/update/', user_api.user_update, name='user_update'),
    path('users/<int:user_id>/delete/', user_api.user_delete, name='user_delete'),
    path('users/<int:user_id>/change-password/', user_api.change_password, name='change_password'),
    path('users/<int:user_id>/change-group/', user_api.change_user_group, name='change_user_group'),
    path('users/available-for-group/<int:group_id>/', user_api.available_users_for_group, name='available_users_for_group'),
    
    path('groups/', group_views.group_list, name='group_list'),
    path('groups/create/', group_api.group_create, name='group_create'),
    path('groups/<int:group_id>/', group_views.group_detail_api, name='group_detail_api'),
    path('groups/<int:group_id>/update/', group_api.group_update, name='group_update'),
    path('groups/<int:group_id>/members/', group_views.group_members, name='group_members'),
]
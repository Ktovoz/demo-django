from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from django.views.generic import RedirectView

app_name = 'demo'

urlpatterns = [

    path('init/<str:password>/', views.init_system, name='init_system'),
    path('init/<str:password>', RedirectView.as_view(permanent=True, pattern_name='demo:init_system'), name='init_system_redirect'),
    
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', LogoutView.as_view(next_page='demo:login', template_name='demo/login.html'), name='logout'),
    

    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:user_id>/', views.user_detail_api, name='user_detail_api'),
    path('users/<int:user_id>/update/', views.user_update, name='user_update'),
    path('users/<int:user_id>/delete/', views.user_delete, name='user_delete'),
    path('users/<int:user_id>/change-password/', views.change_password, name='change_password'),
    path('users/<int:user_id>/change-group/', views.change_user_group, name='change_user_group'),
    path('users/available-for-group/<int:group_id>/', views.available_users_for_group, name='available_users_for_group'),
    

    path('groups/', views.group_list, name='group_list'),
    path('groups/create/', views.group_create, name='group_create'),
    path('groups/<int:group_id>/', views.group_detail_api, name='group_detail_api'),
    path('groups/<int:group_id>/update/', views.group_update, name='group_update'),
    path('groups/<int:group_id>/members/', views.group_members, name='group_members'),
] 
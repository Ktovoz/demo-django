# 项目概述

这是一个基于Django框架构建的现代化Web应用程序项目，提供完整的用户管理、认证系统和RESTful API接口。项目使用Django REST框架提供API端点，所有API均返回JSON格式数据。

## 主要特性

- 基于Token的用户认证系统
- 完整的用户和用户组管理
- RESTful API设计
- 内置Django Admin后台
- Docker容器化支持
- 完整的测试覆盖

# 技术栈

- Python 3.10
- Django 4.2
- Django REST Framework
- SQLite (开发环境) / PostgreSQL (生产环境)
- Gunicorn (生产环境WSGI服务器)
- Docker

# 目录结构

```
DjangoProject/
├── .github/                # GitHub工作流配置
│   └── workflows/
│       └── docker-image.yml
├── DjangoProject/         # Django项目主目录
│   ├── __init__.py
│   ├── asgi.py           # ASGI配置
│   ├── settings.py       # 项目设置
│   ├── urls.py           # 主URL路由
│   └── wsgi.py           # WSGI配置
├── demo/                  # Django应用目录
│   ├── admin.py          # 管理后台配置
│   ├── apps.py           # 应用配置
│   ├── models.py         # 数据模型
│   ├── views.py          # 视图函数
│   └── urls.py           # 应用URL路由
├── templates/             # 模板文件目录
├── static/                # 静态文件目录
├── media/                 # 媒体文件目录
├── data/                  # 数据目录
├── requirements.txt       # Python依赖
├── Dockerfile            # Docker构建文件
├── entrypoint.sh         # Docker容器启动脚本
└── manage.py             # Django管理脚本
```

# 开发环境搭建

## 依赖安装

```bash
pip install -r requirements.txt
```

## 数据库初始化

```bash
python manage.py migrate
```

## 创建超级用户

```bash
python manage.py createsuperuser
```

## 启动开发服务器

```bash
python manage.py runserver
```

# Docker部署

## 构建镜像

```bash
docker build -t djangoapp .
```

## 运行容器

```bash
docker run -p 8000:8000 djangoapp
```

# API接口

## 用户管理API

- `POST /demo/users/create/` - 创建用户
- `GET /demo/users/<user_id>/` - 获取用户详情
- `POST /demo/users/<user_id>/update/` - 更新用户信息

## 用户组管理API

- `GET /demo/groups/` - 获取用户组列表
- `GET /demo/groups/<group_id>/` - 获取组详情
- `POST /demo/groups/create/` - 创建用户组

# 开发约定

- 使用Django的基于类的视图和函数视图混合开发模式
- 遵循Django的MTV架构模式
- 使用Django的权限系统进行访问控制
- 所有API接口返回JSON格式数据
- 使用Docker进行容器化部署
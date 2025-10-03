# Django项目开发指南

## 项目概述

这是一个基于Django 4.2框架构建的现代化Web应用程序，主要提供用户管理、认证系统和RESTful API接口。项目使用SQLite作为数据库，支持Docker容器化部署。

## 开发环境命令

### 基础开发命令
```bash
# 安装依赖
pip install -r requirements.txt

# 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 启动开发服务器
python manage.py runserver

# 收集静态文件（生产环境）
python manage.py collectstatic

# Django shell
python manage.py shell
```

### 测试相关命令
```bash
# 运行所有测试
python manage.py test

# 运行特定应用的测试
python manage.py test demo

# 运行测试并显示覆盖率
coverage run --source='.' manage.py test
coverage report
```

### Docker命令
```bash
# 构建镜像
docker build -t djangoapp .

# 运行容器
docker run -p 8000:8000 djangoapp

# 后台运行容器
docker run -d -p 8000:8000 --name django-container djangoapp
```

## 项目架构

### 高级架构
```
DjangoProject/
├── DjangoProject/           # 项目配置目录
│   ├── settings.py         # 主配置文件
│   ├── urls.py             # 主URL路由
│   ├── wsgi.py             # WSGI配置
│   └── asgi.py             # ASGI配置
├── demo/                   # 核心应用
│   ├── views.py            # 视图函数（向后兼容）
│   ├── views/              # 模块化视图
│   │   ├── auth_views.py   # 认证相关视图
│   │   ├── user_views.py   # 用户管理视图
│   │   ├── group_views.py  # 用户组管理视图
│   │   └── system_views.py # 系统功能视图
│   ├── api/                # API接口
│   │   ├── user_api.py     # 用户API
│   │   └── group_api.py    # 用户组API
│   ├── templates/          # 模板文件
│   ├── static/             # 静态文件
│   └── logger.py           # 日志配置
├── data/                   # 数据目录
│   └── db.sqlite3          # SQLite数据库
├── logs/                   # 日志目录
└── media/                  # 媒体文件目录
```

### 代码架构特点
- **模块化设计**: 视图函数按功能分离到不同模块
- **API分离**: API接口单独组织，便于维护
- **权限控制**: 基于Django权限系统的细粒度控制
- **日志系统**: 使用loguru实现分级日志记录

## 重要文件说明

### 配置文件

#### `DjangoProject/settings.py`
- Django版本: 4.2+
- 数据库: SQLite (位于 `data/db.sqlite3`)
- 中间件: 包含CORS支持
- 静态文件: 支持开发和生产环境配置
- 日志: 基础控制台日志配置
- 安全: DEBUG=False，允许所有主机

#### `requirements.txt`
- Django >=4.2,<5.0
- gunicorn >=21.2.0 (生产服务器)
- psycopg2-binary >=2.9.1 (PostgreSQL支持)
- django-cors-headers >=4.7.0 (CORS支持)
- loguru >=0.7.0 (日志系统)

### 核心应用文件

#### `demo/views.py`
- 向后兼容的主视图文件
- 重新导出各个模块的视图函数
- 保持URL路由的兼容性

#### `demo/logger.py`
- 基于loguru的日志配置
- 支持控制台和文件日志
- 日志轮转: 500MB自动切换，保留30天
- 错误日志单独记录，支持回溯和诊断

#### `demo/urls.py`
- 应用URL路由配置
- 包含完整的用户和用户组管理API
- 系统初始化端点

## Django特定功能

### 用户权限系统
项目实现了三层用户权限：
- **超级管理员**: 完整的用户和组管理权限
- **管理员**: 用户增删改查和组查看权限
- **普通用户**: 基础查看权限

### API端点
主要的RESTful API端点：
- `/demo/users/` - 用户列表和创建
- `/demo/users/<id>/` - 用户详情、更新、删除
- `/demo/groups/` - 用户组管理
- `/demo/init/<password>/` - 系统初始化

### 日志系统
使用loguru实现的高级日志功能：
- 异步日志写入
- 自动日志轮转和压缩
- 分级日志记录（INFO、ERROR等）
- 详细的错误回溯信息

### 数据库配置
- 开发环境: SQLite数据库
- 数据文件位置: `data/db.sqlite3`
- 支持PostgreSQL（通过psycopg2-binary）

## 开发注意事项

### 权限管理
- 所有管理功能都需要相应权限
- 普通用户不能修改超级管理员
- 用户不能删除自己的账户

### 安全配置
- CSRF保护已启用
- CORS配置允许所有源（开发环境）
- 受信任的域名配置在 `CSRF_TRUSTED_ORIGINS`

### 系统初始化
- 使用 `/demo/init/admin123/` 初始化系统
- 自动创建默认用户组和超级管理员账户
- 默认管理员账号: admin/admin

### 日志调试
- 所有操作都有详细的日志记录
- 日志文件位置: `logs/django.log` 和 `logs/error.log`
- 使用 `logger.info()`, `logger.warning()`, `logger.error()` 记录操作

## 生产环境部署

### 环境变量
建议设置以下环境变量：
- `DJANGO_SETTINGS_MODULE`: 设置模块路径
- `SECRET_KEY`: 生产环境密钥
- `DEBUG`: 设置为False
- `ALLOWED_HOSTS`: 配置允许的主机

### 静态文件
```bash
python manage.py collectstatic --noinput
```

### 数据库
生产环境建议使用PostgreSQL，需要修改 `settings.py` 中的数据库配置。

### 日志目录
确保 `logs/` 目录有写入权限，用于存储应用日志。
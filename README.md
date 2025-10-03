# Django Hub - 现代化用户管理平台

<div align="center">
  <img src="https://www.djangoproject.com/m/img/logos/django-logo-positive.png" alt="Django" width="300">

  <p align="center">
    <img src="https://img.shields.io/badge/Django-4.2+-green?logo=django&style=flat-square" alt="Django"/>
    <img src="https://img.shields.io/badge/Python-3.8+-blue?logo=python&style=flat-square" alt="Python"/>
    <img src="https://img.shields.io/badge/SQLite-3.0+-blue?logo=sqlite&style=flat-square" alt="SQLite"/>
    <img src="https://img.shields.io/badge/Loguru-0.7+-orange?style=flat-square" alt="Loguru"/>
    <br/>
    <img src="https://img.shields.io/badge/Docker-Ready-blue?logo=docker&style=flat-square" alt="Docker"/>
    <img src="https://img.shields.io/badge/Gunicorn-WSGI-green?style=flat-square" alt="Gunicorn"/>
    <img src="https://img.shields.io/github/actions/workflow/status/ktovoz/demo-django/docker-image.yml?style=flat-square&logo=github" alt="Build Status"/>
    <img src="https://img.shields.io/badge/version-2.0.0-blue?style=flat-square" alt="Version"/>
    <img src="https://img.shields.io/badge/license-MIT-orange?style=flat-square" alt="License"/>
  </p>
</div>

<hr style="height: 2px; background: #ddd;">

## 🚀 项目概述

**Django Hub** 是一个基于Django 4.2框架构建的**现代化用户管理平台**，采用企业级架构设计，提供完整的用户管理、权限控制、认证系统和RESTful API接口。该项目展示了现代Django应用的最佳实践，包括模块化设计、高级日志记录、容器化部署等特性。

### ✨ 核心特性

#### 🏗️ 架构设计
- **📦 模块化设计**: 视图层按功能分离，API接口独立组织
- **🔧 向后兼容**: 保持URL路由兼容性的同时支持新架构
- **🛡️ 权限系统**: 基于Django原生权限的三层权限控制
- **📊 高级日志**: 基于Loguru的分级日志、自动轮转和错误回溯
- **🎯 客户端追踪**: 支持客户端IP、User-Agent等信息记录

#### 💼 业务功能
- **👥 用户管理**: 完整的用户CRUD操作，支持用户状态管理
- **🏢 用户组管理**: 用户组的创建、更新和成员管理
- **🔐 认证系统**: 用户注册、登录、登出和用户名可用性检查
- **⚙️ 系统初始化**: 一键初始化系统数据和配置
- **🔑 密码管理**: 安全的密码修改和重置功能

#### 🛠️ 技术特性
- **🌐 RESTful API**: 标准的API设计，支持JSON格式
- **🔒 安全配置**: CSRF保护、CORS支持、安全头设置
- **🐳 容器化**: 完整的Docker部署方案
- **📝 详细日志**: 操作日志、错误追踪、性能监控
- **🔍 错误回溯**: 详细的错误追踪和诊断功能

#### 🎨 用户体验
- **📱 响应式设计**: 支持多种设备和屏幕尺寸
- **🎭 现代UI**: 清新简洁的用户界面，优化的视觉效果
- **⚡ 实时交互**: 用户名可用性实时检查
- **🌍 国际化支持**: 完整的中文本地化

#### 🚀 最新功能
- **🔍 用户名检查**: 实时检查用户名可用性，提供即时反馈
- **🎨 界面优化**: 重新设计的登录和注册页面，提升用户体验
- **📊 管理界面**: 增强的用户管理界面，支持更直观的操作
- **🛡️ 安全增强**: 改进的认证系统和权限验证机制

<hr style="height: 1px; background: #eee;">

## 📚 技术栈

| 组件 | 版本 | 说明 |
|------|------|------|
| **框架** | Django 4.2+ | Python Web框架 |
| **数据库** | SQLite 3.0+ | 开发数据库，支持生产环境PostgreSQL |
| **Web服务器** | Gunicorn 21.2+ | 生产环境WSGI服务器 |
| **日志系统** | Loguru 0.7+ | 高级Python日志库 |
| **跨域支持** | django-cors-headers 4.7+ | CORS中间件 |
| **容器化** | Docker 24.0+ | 容器化部署支持 |

## 🔌 API接口文档

项目提供完整的RESTful API接口，所有API均返回JSON格式数据，支持CORS跨域请求。

### 📋 API响应格式

所有API接口统一返回以下JSON格式：

```json
{
  "status": "success|error",
  "message": "string",
  "data": "object|array|null",
  "errors": "object|null"
}
```

**状态码说明：**
- `200`: 成功
- `400`: 请求参数错误
- `401`: 未认证
- `403`: 权限不足
- `404`: 资源不存在
- `500`: 服务器内部错误

### 🔐 认证API

#### 用户登录
```http
POST /demo/login/
Content-Type: application/json

{
  "username": "string",
  "password": "string"
}
```

**响应示例：**
```json
{
  "status": "success",
  "message": "登录成功",
  "data": {
    "user_id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "is_superuser": true
  }
}
```

#### 用户注册
```http
POST /demo/register/
Content-Type: application/json

{
  "username": "string",
  "password": "string",
  "email": "string"
}
```

#### 用户名可用性检查
```http
GET /demo/check-username/?username=<username>
```

**响应示例：**
```json
{
  "available": true,
  "message": "用户名可用"
}
```

#### 用户登出
```http
POST /demo/logout/
```

### 👤 用户管理API

#### 获取用户列表
```http
GET /demo/users/
```

#### 用户API接口
```http
GET /demo/users/api/
```

#### 创建用户
```http
POST /demo/users/create/
Content-Type: application/json

{
  "username": "string",
  "password": "string",
  "email": "string",
  "group_id": "integer (optional)",
  "is_active": "boolean (optional)"
}
```

#### 获取用户详情
```http
GET /demo/users/<user_id>/
```

#### 更新用户信息
```http
POST /demo/users/<user_id>/update/
Content-Type: application/json

{
  "username": "string (optional)",
  "email": "string (optional)",
  "password": "string (optional)",
  "group_id": "integer (optional)",
  "is_active": "boolean (optional)"
}
```

#### 修改用户密码
```http
POST /demo/users/<user_id>/change-password/
Content-Type: application/json

{
  "new_password": "string"
}
```

#### 删除用户
```http
DELETE /demo/users/<user_id>/delete/
```

#### 修改用户组
```http
POST /demo/users/<user_id>/change-group/
Content-Type: application/json

{
  "group_id": "integer"
}
```

#### 获取可分配用户
```http
GET /demo/users/available-for-group/<group_id>/
```

### 👥 用户组管理API

#### 获取用户组列表
```http
GET /demo/groups/
```

#### 获取用户组详情
```http
GET /demo/groups/<group_id>/
```

#### 获取用户组详情API
```http
GET /demo/groups/<group_id>/members/
```

#### 创建用户组
```http
POST /demo/groups/create/
Content-Type: application/json

{
  "name": "string"
}
```

#### 更新用户组
```http
POST /demo/groups/<group_id>/update/
Content-Type: application/json

{
  "name": "string"
}
```

#### 删除用户组
```http
DELETE /demo/groups/<group_id>/delete/
```

### ⚙️ 系统管理API

#### 系统初始化
```http
POST /demo/init/<password>/
```

**初始化内容：**
- 创建默认用户组（超级管理员、管理员、普通用户）
- 创建超级管理员账户（admin/admin）
- 配置基础权限

#### 日志测试
```http
GET /demo/test-logging/
```

### 🔒 权限说明

#### 权限级别
- **超级管理员**: 所有权限
- **管理员**: 用户管理权限、用户组查看权限
- **普通用户**: 基础查看权限

#### 权限验证
所有API接口都会验证用户权限，确保用户只能访问有权限的资源。

<hr style="height: 1px; background: #eee;">

## 📂 项目架构

```
django-hub/
├── .github/                     # GitHub Actions 工作流
│   └── workflows/
│       └── docker-image.yml     # Docker镜像构建配置
├── DjangoProject/              # Django项目核心配置
│   ├── __init__.py
│   ├── asgi.py                 # ASGI异步服务器配置
│   ├── settings.py             # 项目主配置文件
│   ├── urls.py                 # 主URL路由配置
│   └── wsgi.py                 # WSGI服务器配置
├── demo/                       # 主应用模块
│   ├── admin.py                # Django Admin后台配置
│   ├── apps.py                 # 应用配置类
│   ├── models.py               # 数据模型定义
│   ├── logger.py               # Loguru日志配置
│   ├── views.py                # 视图函数兼容层
│   ├── urls.py                 # 应用URL路由
│   ├── tests.py                # 测试文件
│   ├── api/                    # API接口层
│   │   ├── __init__.py
│   │   ├── user_api.py         # 用户相关API
│   │   ├── group_api.py        # 用户组相关API
│   │   └── serializers.py      # API数据序列化器
│   ├── views/                  # 视图层模块
│   │   ├── __init__.py
│   │   ├── auth_views.py       # 认证相关视图
│   │   ├── user_views.py       # 用户管理视图
│   │   ├── group_views.py      # 用户组管理视图
│   │   └── system_views.py     # 系统管理视图
│   ├── migrations/             # 数据库迁移文件
│   │   └── __init__.py
│   ├── static/                 # 静态文件资源
│   │   ├── css/                # 样式文件
│   │   │   ├── style.css       # 主样式
│   │   │   ├── admin-style.css # 管理后台样式
│   │   │   ├── login.css       # 登录页面样式
│   │   │   ├── register.css    # 注册页面样式
│   │   │   └── user-management.css  # 用户管理样式
│   │   └── js/                 # JavaScript文件
│   │       ├── main.js         # 主要JavaScript功能
│   │       └── user-management.js  # 用户管理交互
│   └── templates/              # 模板文件
│       ├── demo/               # 应用模板
│       │   ├── home.html       # 首页模板
│       │   ├── login.html      # 登录页面
│       │   ├── register.html   # 注册页面
│       │   ├── user_detail.html # 用户详情页面
│       │   └── user_management.html  # 用户管理页面
│       └── base.html           # 基础模板
├── data/                       # 数据存储目录
│   └── db.sqlite3              # SQLite数据库文件
├── logs/                       # 日志文件目录
│   ├── django.log              # 应用日志
│   └── error.log               # 错误日志
├── staticfiles/                # 静态文件收集目录
├── media/                      # 媒体文件目录
├── .codebuddy/                 # 代码助手配置
├── manage.py                   # Django管理脚本
├── requirements.txt            # Python依赖包列表
├── Dockerfile                  # Docker构建文件
├── entrypoint.sh               # 容器启动脚本
├── CLAUDE.md                   # Claude Code 开发指南
├── CODEBUDDY.md                # 代码助手配置
└── README.md                   # 项目说明文档
```

### 🏗️ 架构设计说明

#### 1. 分层架构
- **API层**: `demo/api/` - 纯粹的RESTful API接口
- **视图层**: `demo/views/` - 按功能模块化的视图函数
- **兼容层**: `demo/views.py` - 保持向后兼容的重新导出
- **模板层**: `demo/templates/` - 用户界面模板
- **静态层**: `demo/static/` - 前端资源文件

#### 2. 核心模块
- **认证模块**: `auth_views.py` - 用户登录、注册、首页、登出
- **用户模块**: `user_views.py` - 用户CRUD操作、密码管理
- **用户组模块**: `group_views.py` - 用户组管理、成员管理
- **系统模块**: `system_views.py` - 系统初始化、状态检查

#### 3. 数据模型
- **User**: Django内置用户模型，扩展了用户管理功能
- **Group**: Django内置组模型，支持用户组管理
- **权限系统**: 基于Django原生权限的三层权限控制

#### 4. 日志系统
- **分级日志**: INFO级别应用日志，ERROR级别错误日志
- **自动轮转**: 日志文件达到500MB自动轮转
- **历史保留**: 保留30天的日志历史
- **压缩存储**: 历史日志自动压缩为zip格式
- **客户端追踪**: 支持IP、User-Agent等信息记录

#### 5. 前端架构
- **响应式设计**: 支持多种设备和屏幕尺寸
- **模块化CSS**: 按功能分离的样式文件
- **现代UI**: 清新简洁的用户界面
- **交互体验**: 优化的用户交互反馈

#### 6. 安全特性
- **CSRF保护**: 防止跨站请求伪造
- **CORS支持**: 跨域资源共享配置
- **密码加密**: 安全的密码存储和验证
- **权限验证**: 细粒度的权限控制系统
- **输入验证**: 防止SQL注入和XSS攻击

#### 7. API设计原则
- **RESTful**: 遵循REST设计原则
- **统一响应**: 标准化的JSON响应格式
- **错误处理**: 完善的错误处理和状态码
- **文档化**: 清晰的API文档和示例
- **版本控制**: 支持API版本管理

#### 8. 部署架构
- **容器化**: Docker容器化部署
- **可扩展**: 支持水平扩展
- **监控**: 日志监控和性能监控
- **备份**: 数据备份和恢复机制
- **CI/CD**: 自动化构建和部署

<hr style="height: 1px; background: #eee;">

## 🚀 快速开始

### 📋 环境要求

- **Python**: 3.8+
- **Django**: 4.2+
- **数据库**: SQLite 3.0+ (开发) / PostgreSQL (生产)
- **操作系统**: Windows / macOS / Linux
- **内存**: 最低 2GB，推荐 4GB+
- **存储**: 最低 5GB 可用空间

### 💻 本地开发

#### 1. 克隆项目
```bash
git clone https://github.com/ktovoz/demo-django-hub.git
cd demo-django-hub
```

#### 2. 创建虚拟环境
```bash
# 使用 venv
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

#### 3. 安装依赖
```bash
pip install -r requirements.txt
```

#### 4. 环境配置
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑环境变量
# DEBUG=True
# SECRET_KEY=your-secret-key-here
# ALLOWED_HOSTS=localhost,127.0.0.1
```

#### 5. 数据库初始化
```bash
# 运行数据库迁移
python manage.py migrate

# 初始化系统 (推荐使用URL方式)
# 访问 http://localhost:8000/demo/init/admin123/ 来初始化系统
# 或者使用Django shell
python manage.py shell
>>> from demo.views.system_views import init_system
>>> init_system()

# 创建超级用户账户 (如果未通过初始化创建)
python manage.py createsuperuser
```

#### 6. 启动开发服务器
```bash
python manage.py runserver 0.0.0.0:8000
```

#### 7. 访问应用
- **应用首页**: http://localhost:8000/demo/
- **登录页面**: http://localhost:8000/demo/login/
- **注册页面**: http://localhost:8000/demo/register/
- **用户管理**: http://localhost:8000/demo/users/
- **管理后台**: http://localhost:8000/admin/
- **系统初始化**: http://localhost:8000/demo/init/admin123/

#### 8. 测试功能
- **日志测试**: http://localhost:8000/demo/test-logging/
- **用户名检查**: http://localhost:8000/demo/check-username/?username=testuser

### 🐳 Docker 部署

#### 1. 快速启动
```bash
# 构建镜像
docker build -t django-hub .

# 运行容器
docker run -d \
  --name django-hub \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  django-hub
```

#### 2. Docker Compose 部署
```bash
# 使用 docker-compose 启动
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

#### 3. 生产环境配置
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  django-hub:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - SECRET_KEY=${SECRET_KEY}
      - ALLOWED_HOSTS=${ALLOWED_HOSTS}
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
```

### 🔧 配置说明

#### 环境变量配置
```bash
# .env 文件示例
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
# 数据库配置
DB_NAME=django_hub
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
```

#### 数据库配置
开发环境使用SQLite，生产环境建议使用PostgreSQL：

```python
# PostgreSQL 配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'django_hub'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'password'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

#### 日志配置
```python
# 日志级别设置
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
LOG_FILE = os.environ.get('LOG_FILE', 'logs/django.log')
ERROR_LOG_FILE = os.environ.get('ERROR_LOG_FILE', 'logs/error.log')
```

### 🚀 生产部署

#### 云服务器部署
```bash
# 1. 更新系统
sudo apt update && sudo apt upgrade -y

# 2. 安装必要软件
sudo apt install python3-pip python3-venv nginx postgresql

# 3. 克隆项目
git clone https://github.com/ktovoz/demo-django-hub.git
cd demo-django-hub

# 4. 配置环境
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 5. 配置数据库
sudo -u postgres createdb django_hub
sudo -u postgres createuser --interactive

# 6. 运行迁移
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

#### Nginx 配置
```nginx
# /etc/nginx/sites-available/django-hub
server {
    listen 80;
    server_name yourdomain.com;

    location /static/ {
        alias /path/to/project/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /path/to/project/media/;
        expires 1y;
        add_header Cache-Control "public";
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### Gunicorn 服务配置
```ini
# /etc/systemd/system/django-hub.service
[Unit]
Description=Django Hub Gunicorn Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/project
ExecStart=/path/to/venv/bin/gunicorn \
    --workers 3 \
    --bind 127.0.0.1:8000 \
    --access-logfile - \
    --error-logfile - \
    DjangoProject.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

#### SSL 证书配置
```bash
# 使用 Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com

# 自动续期
sudo crontab -e
# 添加以下行
0 12 * * * /usr/bin/certbot renew --quiet
```

## 🧪 测试

### 运行测试
```bash
# 运行所有测试
python manage.py test

# 运行特定应用测试
python manage.py test demo

# 运行测试并生成覆盖率报告
coverage run --source='.' manage.py test
coverage report
coverage html
```

### 测试数据
```bash
# 加载测试数据
python manage.py loaddata fixtures/test_data.json

# 创建测试用户
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.create_user('testuser', 'test@example.com', 'password')
```

<hr style="height: 1px; background: #eee;">

## 📊 监控与日志

### 日志系统配置

项目使用 **Loguru** 作为日志系统，提供以下功能：

#### 日志级别
- **DEBUG**: 详细的调试信息
- **INFO**: 一般信息记录
- **WARNING**: 警告信息
- **ERROR**: 错误信息
- **CRITICAL**: 严重错误

#### 日志文件
```bash
logs/
├── django.log     # 应用主日志 (INFO级别)
└── error.log      # 错误日志 (ERROR级别)
```

#### 日志配置说明
```python
# demo/logger.py 配置特点
- 自动轮转: 500MB
- 历史保留: 30天
- 压缩存储: zip格式
- 异步写入: 提高性能
- 错误回溯: 详细的错误追踪
```

### 性能监控

#### 开发环境监控
```bash
# 查看Django调试工具栏 (如果安装)
pip install django-debug-toolbar

# 数据库查询监控
python manage.py shell
>>> from django.db import connection
>>> connection.queries  # 查看执行的SQL查询
```

#### 生产环境监控
```bash
# 查看应用日志
tail -f logs/django.log

# 查看错误日志
tail -f logs/error.log

# 监控应用进程
ps aux | grep gunicorn
```

## 🚀 生产部署

### 服务器要求
- **CPU**: 2核心以上
- **内存**: 4GB以上
- **存储**: 20GB以上
- **操作系统**: Ubuntu 20.04+ / CentOS 8+

### Nginx + Gunicorn 部署

#### 1. 安装依赖
```bash
# 安装系统依赖
sudo apt update
sudo apt install python3-pip python3-venv nginx postgresql

# 安装Python依赖
pip install -r requirements.txt
pip install psycopg2-binary
```

#### 2. 配置Gunicorn
```bash
# 创建 gunicorn 配置文件
cat > gunicorn.conf.py << EOF
bind = "127.0.0.1:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
```

#### 3. 配置Nginx
```nginx
# /etc/nginx/sites-available/django-hub
server {
    listen 80;
    server_name yourdomain.com;

    location /static/ {
        alias /path/to/your/project/staticfiles/;
    }

    location /media/ {
        alias /path/to/your/project/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### 4. 创建systemd服务
```ini
# /etc/systemd/system/django-hub.service
[Unit]
Description=Django Hub Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/project
ExecStart=/path/to/venv/bin/gunicorn -c gunicorn.conf.py DjangoProject.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

#### 5. 启动服务
```bash
# 启动并启用服务
sudo systemctl start django-hub
sudo systemctl enable django-hub

# 启动Nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

### SSL证书配置
```bash
# 使用Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

## 🤝 贡献指南

### 开发流程
1. Fork 本仓库
2. 创建功能分支: `git checkout -b feature/amazing-feature`
3. 提交更改: `git commit -m 'Add amazing feature'`
4. 推送分支: `git push origin feature/amazing-feature`
5. 提交Pull Request

### 代码规范
- **Python**: 遵循 PEP 8 规范
- **JavaScript**: 使用 ESLint 检查
- **CSS**: 使用 BEM 命名规范
- **提交信息**: 使用 [Conventional Commits](https://conventionalcommits.org/)

### 代码质量检查
```bash
# 代码格式化
black .
isort .

# 代码检查
flake8 .
pylint demo/

# 安全检查
bandit -r demo/
```

## 📞 支持与反馈

### 获取帮助
- **文档**: 查看 [CLAUDE.md](CLAUDE.md) 获取开发指南
- **Issues**: 在 [GitHub Issues](https://github.com/ktovoz/demo-django-hub/issues) 提交问题
- **Wiki**: 查看 [项目Wiki](https://github.com/ktovoz/demo-django-hub/wiki) 获取更多文档

### 常见问题

#### Q: 如何修改数据库配置？
A: 编辑 `DjangoProject/settings.py` 中的 `DATABASES` 配置。

#### Q: 如何添加新的API接口？
A: 在 `demo/api/` 目录下创建新的API模块，并在 `demo/urls.py` 中添加路由。

#### Q: 如何查看日志？
A: 日志文件位于 `logs/` 目录，使用 `tail -f logs/django.log` 实时查看。

#### Q: 如何部署到生产环境？
A: 参考「生产部署」章节的详细说明。

## 📄 开源协议

本项目采用 **MIT 协议** 开源，详见 [LICENSE](LICENSE) 文件。

---

<div align="center">
  <p>🌟 如果这个项目对您有帮助，请给我们一个 Star！</p>
  <p>Made with ❤️ by Django Hub Team</p>
</div>
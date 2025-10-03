# Django Hub - 企业级用户管理系统

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

**Django Hub** 是一个基于Django框架构建的**企业级用户管理系统**，采用模块化架构设计，提供完整的用户管理、权限控制、认证系统和RESTful API接口。该项目展示了现代Django应用的最佳实践，包括分层架构、高级日志记录、容器化部署等特性。

### ✨ 核心特性

#### 🏗️ 架构设计
- **📦 模块化设计**: 视图层按功能分离，API接口独立组织
- **🔧 向后兼容**: 保持URL路由兼容性的同时支持新架构
- **🛡️ 权限系统**: 基于Django原生权限的三层权限控制
- **📊 高级日志**: 基于Loguru的分级日志、自动轮转和错误回溯

#### 💼 业务功能
- **👥 用户管理**: 完整的用户CRUD操作，支持用户状态管理
- **🏢 用户组管理**: 用户组的创建、更新和成员管理
- **🔐 权限控制**: 细粒度的权限管理系统
- **⚙️ 系统初始化**: 一键初始化系统数据和配置

#### 🛠️ 技术特性
- **🌐 RESTful API**: 标准的API设计，支持JSON格式
- **🔒 安全配置**: CSRF保护、CORS支持、安全头设置
- **🐳 容器化**: 完整的Docker部署方案
- **📝 详细日志**: 操作日志、错误追踪、性能监控

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

项目提供完整的RESTful API接口，所有API均返回JSON格式数据。

### 👤 用户管理API

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

#### 获取用户组成员
```http
GET /demo/groups/<group_id>/members/
```

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

### ⚙️ 系统管理API

#### 系统初始化
```http
POST /demo/init-system/
```

#### 首页
```http
GET /demo/
```

## 📋 API响应格式

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
│   └── static/                 # 静态文件资源
├── data/                       # 数据存储目录
│   └── db.sqlite3              # SQLite数据库文件
├── logs/                       # 日志文件目录
│   ├── django.log              # 应用日志
│   └── error.log               # 错误日志
├── staticfiles/                # 静态文件收集目录
├── templates/                  # 模板文件目录
├── manage.py                   # Django管理脚本
├── requirements.txt            # Python依赖包列表
├── Dockerfile                  # Docker构建文件
├── entrypoint.sh               # 容器启动脚本
├── CLAUDE.md                   # Claude Code 开发指南
└── README.md                   # 项目说明文档
```

### 🏗️ 架构设计说明

#### 1. 分层架构
- **API层**: `demo/api/` - 纯粹的RESTful API接口
- **视图层**: `demo/views/` - 按功能模块化的视图函数
- **兼容层**: `demo/views.py` - 保持向后兼容的重新导出

#### 2. 核心模块
- **认证模块**: `auth_views.py` - 用户登录、注册、首页
- **用户模块**: `user_views.py` - 用户CRUD操作
- **用户组模块**: `group_views.py` - 用户组管理
- **系统模块**: `system_views.py` - 系统初始化

#### 3. 日志系统
- **分级日志**: INFO级别应用日志，ERROR级别错误日志
- **自动轮转**: 日志文件达到500MB自动轮转
- **历史保留**: 保留30天的日志历史
- **压缩存储**: 历史日志自动压缩为zip格式

<hr style="height: 1px; background: #eee;">

## 🚀 快速开始

### 📋 环境要求

- **Python**: 3.8+
- **Django**: 4.2+
- **数据库**: SQLite 3.0+ (开发) / PostgreSQL (生产)
- **操作系统**: Windows / macOS / Linux

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

#### 4. 数据库初始化
```bash
# 运行数据库迁移
python manage.py migrate

# 创建超级用户账户
python manage.py createsuperuser

# 初始化系统数据 (可选)
python manage.py shell
>>> from demo.views.system_views import init_system
>>> init_system()
```

#### 5. 启动开发服务器
```bash
python manage.py runserver 0.0.0.0:8000
```

#### 6. 访问应用
- **应用首页**: http://localhost:8000/demo/
- **管理后台**: http://localhost:8000/admin/
- **API文档**: http://localhost:8000/demo/api/

### 🐳 Docker 部署

#### 1. 构建镜像
```bash
docker build -t django-hub .
```

#### 2. 运行容器
```bash
# 开发环境
docker run -p 8000:8000 django-hub

# 生产环境 (带数据持久化)
docker run -d \
  --name django-hub \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  django-hub
```

#### 3. Docker Compose 部署
```bash
# 如果有 docker-compose.yml
docker-compose up -d
```

### 🔧 配置说明

#### 环境变量配置
```bash
# 创建 .env 文件
echo "DEBUG=False" > .env
echo "SECRET_KEY=your-secret-key-here" >> .env
echo "ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com" >> .env
```

#### 数据库配置
开发环境使用SQLite，生产环境可配置PostgreSQL：

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django_hub',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
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
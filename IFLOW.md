# 项目概述

**Django Hub** 是一个基于Django 4.2框架构建的现代化用户管理平台，采用企业级架构设计，提供完整的用户管理、权限控制、认证系统和RESTful API接口。该项目展示了现代Django应用的最佳实践，包括模块化设计、高级日志记录、容器化部署等特性。

## 主要特性

### 🏗️ 架构设计
- **📦 模块化设计**: 视图层按功能分离，API接口独立组织
- **🔧 向后兼容**: 保持URL路由兼容性的同时支持新架构
- **🛡️ 权限系统**: 基于Django原生权限的三层权限控制
- **📊 高级日志**: 基于Loguru的分级日志、自动轮转和错误回溯
- **🎯 客户端追踪**: 支持客户端IP、User-Agent等信息记录

### 💼 业务功能
- **👥 用户管理**: 完整的用户CRUD操作，支持用户状态管理
- **🏢 用户组管理**: 用户组的创建、更新和成员管理
- **🔐 权限控制**: 细粒度的权限管理系统
- **⚙️ 系统初始化**: 一键初始化系统数据和配置
- **🔑 密码管理**: 安全的密码修改和重置功能

### 🛠️ 技术特性
- **🌐 RESTful API**: 标准的API设计，支持JSON格式
- **🔒 安全配置**: CSRF保护、CORS支持、安全头设置
- **🐳 容器化**: 完整的Docker部署方案
- **📝 详细日志**: 操作日志、错误追踪、性能监控
- **🔍 错误回溯**: 详细的错误追踪和诊断功能

### 🎨 用户体验
- **📱 响应式设计**: 支持多种设备和屏幕尺寸
- **🎭 现代UI**: 清新简洁的用户界面
- **⚡ 快速响应**: 优化的前端性能
- **🌍 国际化支持**: 完整的中文本地化

## 技术栈

| 组件 | 版本 | 说明 |
|------|------|------|
| **框架** | Django 4.2+ | Python Web框架 |
| **数据库** | SQLite 3.0+ | 开发数据库，支持生产环境PostgreSQL |
| **Web服务器** | Gunicorn 21.2+ | 生产环境WSGI服务器 |
| **日志系统** | Loguru 0.7+ | 高级Python日志库 |
| **跨域支持** | django-cors-headers 4.7+ | CORS中间件 |
| **容器化** | Docker 24.0+ | 容器化部署支持 |

## 目录结构

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
│   ├── static/                 # 静态文件资源
│   │   ├── css/                # 样式文件
│   │   │   ├── style.css       # 主样式
│   │   │   ├── user-management.css  # 用户管理样式
│   │   │   └── register.css    # 注册页面样式
│   │   └── js/                 # JavaScript文件
│   └── templates/              # 模板文件
│       ├── demo/               # 应用模板
│       │   ├── home.html       # 首页模板
│       │   ├── login.html      # 登录页面
│       │   ├── register.html   # 注册页面
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
├── README.md                   # 项目说明文档
└── 注册页面样式优化与交互实现.md  # 开发文档
```

## 开发环境搭建

### 环境要求

- **Python**: 3.8+
- **Django**: 4.2+
- **数据库**: SQLite 3.0+ (开发) / PostgreSQL (生产)
- **操作系统**: Windows / macOS / Linux
- **内存**: 最低 2GB，推荐 4GB+
- **存储**: 最低 5GB 可用空间

### 依赖安装

```bash
pip install -r requirements.txt
```

### 数据库初始化

```bash
python manage.py migrate
```

### 创建超级用户

```bash
python manage.py createsuperuser
```

### 启动开发服务器

```bash
python manage.py runserver 0.0.0.0:8000
```

## Docker部署

### 构建镜像

```bash
docker build -t django-hub .
```

### 运行容器

```bash
docker run -d \
  --name django-hub \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  django-hub
```

## API接口

项目提供完整的RESTful API接口，所有API均返回JSON格式数据，支持CORS跨域请求。

### API响应格式

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

### 认证API

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

#### 用户登出
```http
POST /demo/logout/
```

### 用户管理API

#### 获取用户列表
```http
GET /demo/users/
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

#### 获取可分配用户
```http
GET /demo/users/available-for-group/<group_id>/
```

### 用户组管理API

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

#### 删除用户组
```http
DELETE /demo/groups/<group_id>/delete/
```

#### 获取用户组成员
```http
GET /demo/groups/<group_id>/members/
```

### 系统管理API

#### 系统初始化
```http
POST /demo/init/<password>/
```

#### 系统状态检查
```http
GET /demo/system/status/
```

#### 获取系统信息
```http
GET /demo/system/info/
```

## 开发约定

- 使用Django的基于类的视图和函数视图混合开发模式
- 遵循Django的MTV架构模式
- 使用Django的权限系统进行访问控制
- 所有API接口返回JSON格式数据
- 使用Docker进行容器化部署
- 采用模块化设计，按功能分离视图和API
- 使用Loguru进行高级日志记录
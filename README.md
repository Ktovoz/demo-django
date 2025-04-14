# DjangoProject 

<div align="center">
  <img src="https://www.djangoproject.com/m/img/logos/django-logo-positive.png" alt="Django" width="300">
  
  <p align="center">
    <img src="https://img.shields.io/badge/Django-4.2-green?logo=django&style=flat-square" alt="Django"/>
    <img src="https://img.shields.io/badge/Python-3.10-blue?logo=python&style=flat-square" alt="Python"/>
    <img src="https://img.shields.io/badge/Docker-24.0-blue?logo=docker&style=flat-square" alt="Docker"/>
    <br/>
    <img src="https://img.shields.io/github/actions/workflow/status/ktovoz/demo-django/docker-image.yml?style=flat-square&logo=github" alt="Build Status"/>
    <img src="https://img.shields.io/badge/version-1.0.0-blue?style=flat-square" alt="Version"/>
    <img src="https://img.shields.io/badge/license-MIT-orange?style=flat-square" alt="License"/>
  </p>
</div>

<hr style="height: 2px; background: #ddd;">

## 🚀 项目概述

这是一个基于Django框架构建的现代化Web应用程序项目，提供完整的用户管理、认证系统和RESTful API接口。

### ✨ 主要特性

<table>
  <tr>
    <td>✅ 基于Token的用户认证系统</td>
    <td>✅ 完整的用户和用户组管理</td>
  </tr>
  <tr>
    <td>✅ RESTful API设计</td>
    <td>✅ 内置Django Admin后台</td>
  </tr>
  <tr>
    <td>✅ Docker容器化支持</td>
    <td>✅ 完整的测试覆盖</td>
  </tr>
</table>

<hr style="height: 1px; background: #eee;">

## 📚 API文档

项目使用Django REST框架提供以下API端点，所有API均返回JSON格式数据。

### 👥 用户管理API

<table>
  <thead>
    <tr>
      <th width="15%">方法</th>
      <th width="35%">端点</th>
      <th width="25%">参数</th>
      <th width="25%">返回</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>POST</code></td>
      <td><code>/demo/users/create/</code></td>
      <td><code>username</code>, <code>password</code>, <code>email</code>, <code>group_id</code>, <code>is_active</code></td>
      <td>状态和消息</td>
    </tr>
    <tr>
      <td><code>GET</code></td>
      <td><code>/demo/users/&lt;user_id&gt;/</code></td>
      <td>-</td>
      <td>用户详细信息</td>
    </tr>
    <tr>
      <td><code>POST</code></td>
      <td><code>/demo/users/&lt;user_id&gt;/update/</code></td>
      <td><code>username</code>, <code>email</code>, <code>password</code>, <code>group_id</code>, <code>is_active</code></td>
      <td>状态和消息</td>
    </tr>
  </tbody>
</table>

**示例请求**
```bash
curl -X POST http://localhost:8000/demo/users/create/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"123456","email":"test@example.com"}'
```

### 👥 用户组管理API

<table>
  <thead>
    <tr>
      <th width="15%">方法</th>
      <th width="35%">端点</th>
      <th width="25%">参数</th>
      <th width="25%">返回</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>GET</code></td>
      <td><code>/demo/groups/</code></td>
      <td>-</td>
      <td>用户组列表</td>
    </tr>
    <tr>
      <td><code>GET</code></td>
      <td><code>/demo/groups/&lt;group_id&gt;/</code></td>
      <td>-</td>
      <td>组详情</td>
    </tr>
    <tr>
      <td><code>POST</code></td>
      <td><code>/demo/groups/create/</code></td>
      <td><code>name</code></td>
      <td>状态和消息</td>
    </tr>
  </tbody>
</table>

<hr style="height: 1px; background: #eee;">

## 📂 目录结构

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
└── requirements.txt       # Python依赖
```

<hr style="height: 1px; background: #eee;">

## 🚀 快速开始

### 开发环境

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 运行迁移
python manage.py migrate

# 3. 创建超级用户（可选）
python manage.py createsuperuser

# 4. 启动开发服务器
python manage.py runserver
```

### Docker部署

```bash
# 构建镜像
docker build -t djangoapp .

# 运行容器
docker run -p 8000:8000 djangoapp
```

<hr style="height: 1px; background: #eee;">


## 📄 开源协议

本项目采用 MIT 协议开源，详见 [LICENSE](LICENSE) 文件。
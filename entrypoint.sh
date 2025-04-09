#!/bin/bash

# 等待数据库
echo "等待数据库启动..."
sleep 5

# 执行数据库迁移
echo "执行数据库迁移..."
python manage.py migrate

# 收集静态文件
echo "收集静态文件..."
python manage.py collectstatic --noinput

# 启动开发服务器
echo "启动 Django 开发服务器..."
exec python manage.py runserver 0.0.0.0:8000 
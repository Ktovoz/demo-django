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

# 启动 Gunicorn
echo "启动 Gunicorn 服务器..."
exec gunicorn DjangoProject.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --log-level=info \
    --access-logfile=- \
    --error-logfile=- \
    --capture-output 
#!/bin/bash

# 执行数据库迁移
echo "执行数据库迁移..."
python manage.py migrate

# 启动 Gunicorn
echo "启动 Gunicorn 服务器..."
exec gunicorn DjangoProject.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --log-level=debug \
    --access-logfile=- \
    --error-logfile=- \
    --capture-output 
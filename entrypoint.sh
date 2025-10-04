#!/bin/bash

# 检查是否为生产环境
if [ "$DJANGO_SETTINGS_MODULE" = "DjangoProject.settings_production" ] || [ "$DEBUG" = "False" ]; then
    echo "生产环境模式"
    export DJANGO_SETTINGS_MODULE=DjangoProject.settings_production

    # 执行数据库迁移
    echo "执行数据库迁移..."
    python manage.py migrate

    # 收集静态文件（如果构建时未收集）
    echo "收集静态文件..."
    python manage.py collectstatic --noinput --clear || true

    # 启动 Gunicorn（生产环境）
    echo "启动 Gunicorn 服务器..."
    exec gunicorn DjangoProject.wsgi:application \
        --bind 0.0.0.0:8000 \
        --workers 4 \
        --env DJANGO_SETTINGS_MODULE=DjangoProject.settings_production \
        --log-level=info \
        --access-logfile=- \
        --error-logfile=-
else
    echo "开发环境模式"

    # 执行数据库迁移
    echo "执行数据库迁移..."
    python manage.py migrate

    # 收集静态文件
    echo "收集静态文件..."
    python manage.py collectstatic --noinput --clear || true

    # 启动开发服务器
    echo "启动开发服务器..."
    exec python manage.py runserver 0.0.0.0:8000
fi 
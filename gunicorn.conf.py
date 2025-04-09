import multiprocessing

# 绑定的IP和端口
bind = "0.0.0.0:8000"

# 工作进程数
workers = multiprocessing.cpu_count() * 2 + 1

# 工作模式
worker_class = 'sync'

# 超时时间
timeout = 60

# 最大客户端并发数量
worker_connections = 1000

# 进程名称前缀
proc_name = 'DjangoProject'

# 访问日志文件
accesslog = '/app/logs/access.log'

# 错误日志文件
errorlog = '/app/logs/error.log'

# 日志级别
loglevel = 'info'

# 是否后台运行
daemon = False

# 进程pid文件
pidfile = '/app/gunicorn.pid'

# 启动前是否预加载应用
preload_app = True

# 优雅的重启时间
graceful_timeout = 30 
import multiprocessing

# 绑定的地址和端口
bind = "0.0.0.0:8000"

# worker 相关设置
workers = 3
worker_class = "sync"
timeout = 120
keepalive = 5

# 日志设置
accesslog = "-"
errorlog = "-"
loglevel = "info"

# 进程名称
proc_name = "DjangoProject"

# 优雅的重启
graceful_timeout = 30

# 最大请求数
max_requests = 1000
max_requests_jitter = 50

# 工作模式
preload_app = True

# 守护进程设置
daemon = False

# 用户和组设置
user = "appuser"
group = "appuser"
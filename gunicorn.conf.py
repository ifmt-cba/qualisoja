# Configuração Gunicorn para QualiSoja
# gunicorn.conf.py

import multiprocessing
import os

# Configurações do servidor
bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2

# Configurações do processo
user = "www-data"
group = "www-data"
tmp_upload_dir = None
preload_app = True

# Configurações de log
accesslog = "/var/log/gunicorn/qualisoja_access.log"
errorlog = "/var/log/gunicorn/qualisoja_error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Configurações de segurança
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Configurações de processo
daemon = False
pidfile = "/var/run/gunicorn/qualisoja.pid"
umask = 0
tmp_upload_dir = None

# Configurações de SSL (se necessário)
# certfile = "/etc/ssl/certs/qualisoja.com.br.crt"
# keyfile = "/etc/ssl/private/qualisoja.com.br.key"

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-App.
# @File         : gunicorn
# @Time         : 2019-11-21 11:00
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : https://www.jianshu.com/p/fecf15ad0c9a

import os
import re

dev = False if re.search('.c3_|.c4_', os.environ.get('DOCKER_JOBNAME', '')) else True

# 请求
timeout = 60
keepalive = 5
worker_connections = 1000
bind = '0.0.0.0:8000'

# 日志
accesslog = "./log_cache/access.log" if dev else '/home/work/log/access.log'
errorlog = "./log_cache/error.log" if dev else '/home/work/log/error.log'
pidfile = "./log_cache/gunicorn.pid" if dev else '/home/work/log/gunicorn.log'

# 进程配置
daemon = False  # 开启守护进程（在后台）
x_forwarded_for_header = 'X-FORWARDED-FOR'

# 可控配置
loglevel = os.environ.get('loglevel', 'debug')
workers = os.environ.get('workers', 1)  # multiprocessing.cpu_count() * 2 + 1
threads = os.environ.get('threads', 1)

worker_class_map = {
    'sanic': 'sanic.worker.GunicornWorker',
    'uvicorn': 'uvicorn.workers.UvicornWorker'
}
worker_class = worker_class_map.get('uvicorn', 'gevent')  # -k gevent

# preload==True 会将辅助线程或者进程开在master里，加重master的负担（master最好只是用来负责监听worker进程）
preload_app = os.environ.get('preload_app', True)

if __name__ == '__main__':
    os.system("gunicorn -c gun.py flask_app:app")

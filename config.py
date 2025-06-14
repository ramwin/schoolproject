#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


daemon = False
workers = 16
threads = 4
pidfile = "./deploy/gunicorn.pid"
bind = "0.0.0.0:18123"
accesslog = "log/gunicorn/access.log"
errorlog = "log/gunicorn/error.log"
timeout = 15
max_requests=10240
max_requests_jitter=1024

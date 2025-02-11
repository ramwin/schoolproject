#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


daemon = False
workers = 4
threads = 1
pidfile = "gunicorn.pid"
bind = "0.0.0.0:8000"
accesslog = "log/gunicorn.access.log"
errorlog = "log/gunicorn.error.log"
timeout = 3

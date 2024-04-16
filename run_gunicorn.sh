#!/bin/bash
# Xiang Wang(ramwin@qq.com)

gunicorn schoolproject.wsgi -c gunicorn_config.py

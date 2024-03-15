#!/bin/bash
# Xiang Wang(ramwin@qq.com)


celery multi \
    stop \
    1 2 \
    --app=schoolproject \
    --concurrency=2 \
    --loglevel=INFO \
    --logfile=log/celery.log \
    --pidfile=scripts/celery/%n.pid

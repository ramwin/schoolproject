#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import datetime
import logging
import time

from celery import shared_task


LOGGER = logging.getLogger(__name__)
START_TIME = datetime.datetime.now()


@shared_task
def add(x: int) -> int:
    LOGGER.info("调用add函数: %d, 进程开始于: %s", x, START_TIME)
    if x > 30:
        raise ValueError("数字太大了")
    time.sleep(x)
    LOGGER.info("调用add函数结束: %d", x)
    return x

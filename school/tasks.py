#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import datetime
import logging
import time

from celery import shared_task
from .models import Student


LOGGER = logging.getLogger(__name__)
START_TIME = datetime.datetime.now()


@shared_task
def add(x: int) -> int:
    LOGGER.info("调用add函数: %d, 进程开始于: %s", x, START_TIME)
    if x > 30:
        raise ValueError("数字太大了")
    time.sleep(x)
    LOGGER.info("调用add函数结束: %d", x)
    student, _ = Student.objects.get_or_create()
    # 这里student.的时候，会有类型提示
    student.save()
    return x


@share_task
def test_log() -> None:
    LOGGER.info("我是info")
    LOGGER.warning("我是warning")
    LOGGER.error("我是error, 我要报错了")
    raise ValueError

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import logging
import time
from school.models import Student


LOGGER = logging.getLogger(__name__)


def run():
    start = time.time()
    size = 1000
    for _ in range(size):
        student = Student.objects.get(id=2)
    end = time.time()
    LOGGER.info("数据库查询速度:")
    LOGGER.info("    延迟: %f", (end - start) / size)
    LOGGER.info("    QPS: %f", size / (end - start))

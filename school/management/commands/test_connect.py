#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import logging
import time
from multiprocessing import Pool

from django.core.management.base import BaseCommand
from django.db.backends.signals import connection_created

from school.models.base import Tag


LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.handle2()

    def handle3(self, *args, **kwargs):
        LOGGER.info("测试pool的模式下下, 有多少次, 需要改setting再跑")
        with Pool(5) as p:
            p.map(self.handle_single_task, range(5))

    def handle2(self, *args, **kwargs):
        LOGGER.info(
                "# 测试先父进程连, 然后每个进程单独连, 会不会创建多个链接"
                "## 普通模式, 创建1个链接"
                "## pool模式, 创建4个链接, 只有一个signal"
        )
        LOGGER.info(Tag.objects.count())
        time.sleep(10)
        with Pool(5) as p:
            p.map(self.handle_single_task, range(5))

    def handle1(self, *args, **kwargs):
        LOGGER.info("测试每个进程单独连, 会不会创建多个链接, 会,但是usesysid都一样, signal有5次")
        with Pool(5) as p:
            p.map(self.handle_single_task, range(5))

    @classmethod
    def handle_single_task(cls, pk):
        LOGGER.info("进程: %d", pk)
        for i in range(100):
            LOGGER.info(Tag.objects.count())
            time.sleep(10)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>



import datetime
import logging
import random
import time

from contextvars import ContextVar
from decimal import Decimal
from multiprocessing import Pool
from typing import Tuple, Union, Iterable

from django_commands.commands import LargeQuerysetMutiProcessHandlerCommand
from redis import Redis

from django.core.management.base import BaseCommand, CommandParser
from django.db import connections
from django.utils import timezone

from django_redis import get_redis_connection

import django_commands
from django_commands.utils import iter_large_queryset

from school.models import Student


PROCESS_INITED = ContextVar("inited", default=False)
LOGGER = logging.getLogger(__name__)


class Task:
    queryset = Student.objects.all()
    DURATION = datetime.timedelta(minutes=1)

    def get_tasks(self) -> Iterable[Tuple[int, int]]:
        """use iter_large_queryset util to iterate a large queryset"""
        end_datetime = timezone.now() + self.DURATION
        for queryset in iter_large_queryset(self.queryset, 10):
            if timezone.now() > end_datetime:
                return
            if not queryset:
                return
            assert queryset.first()
            assert queryset.last()
            yield (queryset.first().pk, queryset.last().pk)

    def handle_single_task(self, args):
        time.sleep(random.random())
        LOGGER.info("创建任务: %s", args)

    def handle(self, *args, jobs=None, **kwargs):
        start = timezone.now()
        tasks = self.get_tasks()
        LOGGER.debug("handle task: %s", tasks)
        with Pool(jobs) as p:
            for result in p.imap_unordered(
                self.handle_single_task, tasks):
                LOGGER.info("handle single task done: %s", result)


def run():
    Task().handle()

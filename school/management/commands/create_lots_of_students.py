#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import time
import logging
from faker import Faker

from django.core.management.base import BaseCommand
from django_commands.commands import MultiTimesCommand

from school.models import Student


LOGGER = logging.getLogger(__name__)


class Command(MultiTimesCommand):
    INTERVAL = 0.1

    def handle(self, *args, **kwargs):
        faker = Faker("zh-cn")
        iteration_count = 1
        bulk_size = 2000
        LOGGER.info("创建 %d 个学生", iteration_count * bulk_size)
        start = time.time()
        for _ in range(iteration_count):
            students = []
            for _ in range(bulk_size):
                students.append(
                        Student(
                            name=faker.name(),
                            info={},
                        )
                )
            Student.objects.bulk_create(students)
        end = time.time()
        LOGGER.info("耗时: %d, ops: %s", end - start, bulk_size * iteration_count / (end-start))

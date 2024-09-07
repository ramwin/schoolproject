#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import logging

from django.db import connections
from django_commands.commands import LargeQuerysetMutiProcessHandlerCommand, PROCESS_INITED

from school.models import Student


LOGGER = logging.getLogger(__name__)


class Command(LargeQuerysetMutiProcessHandlerCommand):
    queryset = Student.objects.all()

    def get_tasks(self):
        self.queryset.update(age=0)
        return super().get_tasks()

    @classmethod
    def handle_single_task(cls, duration):
        LOGGER.info("处理范围: %d => %d", duration[0], duration[1])
        student: Student
        for student in cls.queryset.filter(pk__gte=duration[0], pk__lte=duration[1]).order_by("pk"):
            # LOGGER.info("%d", student.id)
            student.age += 1
            student.save()

    def handle(self, *args, **kwargs):
        super().handle(*args, **kwargs)
        LOGGER.info(Student.objects.exclude(age=1))

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import logging

from django_commands.commands import LargeQuerysetMutiProcessHandlerCommand

from school.models import Student


LOGGER = logging.getLogger(__name__)


class Command(LargeQuerysetMutiProcessHandlerCommand):
    queryset = Student.objects.all()

    def handle_single_task(self, startid, endid):
        LOGGER.info(startid, endid)

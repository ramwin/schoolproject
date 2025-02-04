#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import logging

from django.core.management.base import BaseCommand
from django_commands.commands import MultiTimesCommand


LOGGER = logging.getLogger(__name__)


class Command(MultiTimesCommand):

    MAX_TIMES = 3
    help = "测试日志问题"

    def handle(self, *args, **kwargs):
        LOGGER.info("info")
        LOGGER.warning("warning")
        LOGGER.error("error")

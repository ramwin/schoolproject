#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import logging
import colorlog

from django.core.management.base import BaseCommand
from django_commands.commands import MultiTimesCommand


LOGGER = logging.getLogger(__name__)


class Command(MultiTimesCommand):

    MAX_TIMES = 3
    help = "测试日志问题"

    def handle(self, verbosity: int, *args, **kwargs):
        LOGGER.info("verbosity: %d", verbosity)
        if verbosity == 3:
            logging.getLogger('school').setLevel(logging.DEBUG)
            for handler in logging.getLogger("school").handlers:
                if isinstance(handler, colorlog.StreamHandler):
                    handler.setLevel(logging.DEBUG)
            LOGGER.info("因为设置了verbose, 所以下面的debug会展示")
        LOGGER.debug("debug")
        LOGGER.info("info")
        LOGGER.warning("warning")
        LOGGER.error("error")

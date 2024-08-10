#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import logging

from django.core.management.base import BaseCommand


LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):

    help = "测试日志问题"

    def handle(self, *args, **kwargs):
        LOGGER.info("info")
        LOGGER.warning("warning")
        LOGGER.error("error")

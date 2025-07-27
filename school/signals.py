#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import logging

from django.db.backends.signals import connection_created
from django.db.models.signals import post_init, post_save

from .models.base import Tag


LOGGER = logging.getLogger(__name__)


def console(*args, **kwargs) -> None:
    LOGGER.info("args: %s kwargs %s", args, kwargs)


def save_tag(instance: Tag, **kwargs) -> None:
    LOGGER.info("测试一个数据库的数据保存在另外一个数据库是否触发")
    LOGGER.info("kwargs: %s", kwargs)
    LOGGER.info("保存了tag: %s", instance)


connection_created.connect(console)
post_init.connect(console, Tag)
post_save.connect(save_tag, Tag)

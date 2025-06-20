#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import logging

from django.db.backends.signals import connection_created
from django.db.models.signals import post_init

from .models.base import Tag


LOGGER = logging.getLogger(__name__)


def console(*args, **kwargs):
    LOGGER.info("args: %s kwargs %s", args, kwargs)


connection_created.connect(console)
post_init.connect(console, Tag)

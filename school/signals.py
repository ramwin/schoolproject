#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import logging

from django.db.backends.signals import connection_created


LOGGER = logging.getLogger(__name__)


def console(*args, **kwargs):
    LOGGER.info("args: %s kwargs %s", args, kwargs)


connection_created.connect(console)

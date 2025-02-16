#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>



import logging
from django_cache_decorator import django_cache_decorator


LOGGER = logging.getLogger(__name__)


def cache_key_function(function: str, id: int):
    return f"test_key_{id}"


@django_cache_decorator(time=300, cache_type="default", cache_key_function=cache_key_function)
def test_key(id: int):
    LOGGER.info("调用id: %s", id)
    return id + 3


def get_int():
    """
    正式环境返回2, 测试环境返回1
    """
    return 2

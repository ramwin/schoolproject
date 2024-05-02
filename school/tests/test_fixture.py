#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import logging

from django.test import TestCase


LOGGER = logging.getLogger(__name__)


class Test(TestCase):
    fixtures = [
            "school/tests/Student.json",
    ]

    def test(self):
        LOGGER.info("使用fixture也会触发所有的signal哦")

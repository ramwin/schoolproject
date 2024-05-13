#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import logging

from django.test import TestCase
from django.template.loader import get_template


LOGGER = logging.getLogger(__name__)


class Test(TestCase):

    def test(self):
        template = get_template("school/test_filter.html")
        result = template.render(context={"myfloat": 1.1111})
        LOGGER.info(result)

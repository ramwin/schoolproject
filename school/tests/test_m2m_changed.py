#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import logging
from django.test import TestCase

from school.models.relations import Klass, Student


LOGGER = logging.getLogger(__name__)


class Test(TestCase):

    def test(self):
        student1 = Student.objects.create()
        student2 = Student.objects.create()
        klass = Klass.objects.create()
        LOGGER.info("单独add")
        klass.students.add(student1)
        LOGGER.info("set +1 -1")
        klass.students.set([student2])
        LOGGER.info("remove")
        klass.students.remove(student2)
        LOGGER.info("反向 add")
        student1.klass_set.add(klass)

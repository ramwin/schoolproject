#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import logging

from django.db import models
from django.db.models.signals import m2m_changed

from .base import Student


LOGGER = logging.getLogger(__name__)


class Klass(models.Model):
    students = models.ManyToManyField(Student)


def students_changed(
        instance, reverse, action,
        model, pk_set,
        *args, **kwargs):
    LOGGER.debug(
            "变更了: %s, %s, %s, model: %s, pk_set: %s",
            reverse, action, instance,
            model, pk_set,
    )


# 监听Klass是没用的
# m2m_changed.connect(students_changed, Klass)
m2m_changed.connect(students_changed, Klass.students.through)

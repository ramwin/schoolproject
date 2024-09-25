#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import logging

from django.db import models
from django.db.models.signals import m2m_changed, post_save

from .base import Student


LOGGER = logging.getLogger(__name__)


class Parent(models.Model):
    pass


class Child(models.Model):
    mother = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name="children")
    father = models.ForeignKey(Parent, on_delete=models.PROTECT, related_name="+")


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


class Lesson(models.Model):
    title = models.TextField()

    @classmethod
    def post_save(cls, *args, **kwargs):
        LOGGER.info(kwargs)


# 监听Klass是没用的
# m2m_changed.connect(students_changed, Klass)
m2m_changed.connect(students_changed, Klass.students.through)
post_save.connect(Lesson.post_save, Lesson)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import logging

from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.db.models.functions import Lower
from django.db.models.signals import post_save, post_delete

from eventlog.mixins import LoggerMixin


LOGGER = logging.getLogger(__name__)


class Tag(LoggerMixin, models.Model):
    text = models.TextField(default="", blank=True)


class Student(models.Model):
    name = models.TextField()
    code = models.CharField(max_length=15, null=True)
    update_datetime = models.DateTimeField(auto_now=True)
    height = models.IntegerField(null=True)
    info = models.JSONField()

    class Meta:
        constraints = [
                UniqueConstraint(Lower("code"), name="code_unique"),
        ]

    @classmethod
    def post_save(cls, instance: "Student", **kwargs):
        LOGGER.info("学生数据保存了: %s", instance)


class Exam(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.IntegerField()


class TestUnsetField(models.Model):
    # 不设置的话默认是None
    float_field = models.FloatField()
    int_field = models.IntegerField()


def log(**kwargs):
    LOGGER.info("剩余数量: %d", Student.objects.filter(
        id__lte=30
    ).count())


post_save.connect(Student.post_save, Student)
post_delete.connect(log, Student)

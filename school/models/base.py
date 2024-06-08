#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import logging

from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.db.models.functions import Lower
from django.db.models.signals import post_save


LOGGER = logging.getLogger(__name__)


class Student(models.Model):
    name = models.TextField()
    code = models.CharField(max_length=15, null=True)
    update_datetime = models.DateTimeField(auto_now=True)

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


post_save.connect(Student.post_save, Student)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


from django.db import models
from .base import Tag


class Animal(models.Model):
    name = models.TextField()


class Dog(Animal):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

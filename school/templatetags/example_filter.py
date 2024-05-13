#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


from django import template


register = template.Library()


def myformat(value):
    return value + 1


register.filter("myformat", myformat)

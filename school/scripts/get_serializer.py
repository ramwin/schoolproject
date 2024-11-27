#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


from school.models.base import DateTimeModel
from school.serializers import DateTimeModelSerializer


def run():
    print(DateTimeModelSerializer(DateTimeModel.objects.first()).data)

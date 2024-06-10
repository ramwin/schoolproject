#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


from rest_framework import serializers


class AliasSerializer(serializers.Serializer):

    gender = serializers.BooleanField(source="性别")

    class Meta:
        fields = ["gender"]

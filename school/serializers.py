#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


from rest_framework import serializers
from school.models import Student


class AliasSerializer(serializers.Serializer):

    gender = serializers.BooleanField(source="性别")

    class Meta:
        fields = ["gender"]


class StudentUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ["code"]


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ["info"]

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


from rest_framework import serializers
from school.models import Student
from school.models.base import DateTimeModel


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


class DateTimeModelSerializer(serializers.ModelSerializer):
    now = serializers.SerializerMethodField()

    class Meta:
        model = DateTimeModel
        fields = ["now"]

    def get_now(self, obj):
        return obj.now.timestamp()


class TagSerializer(serializers.Serializer):
    text = serializers.CharField()

    class Meta:
        fields = ["text"]

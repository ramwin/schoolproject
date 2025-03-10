#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import logging
from rest_framework import serializers
from school.models import Student
from school.models.base import DateTimeModel, DictModel


LOGGER = logging.getLogger(__name__)


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


class OtherSerializer(serializers.Serializer):
    pop_out_attribute = serializers.CharField()
    integer = serializers.IntegerField()

    class Meta:
        fields = ["pop_out_attribute", "integer"]

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        LOGGER.info("merge之前: %s", ret)
        for key in data.keys() - ret.keys():
            ret[key] = data[key]
        LOGGER.info("merge之后: %s", ret)
        return ret


class DictModelSerializer(serializers.ModelSerializer):
    other = OtherSerializer()

    class Meta:
        model = DictModel
        fields = ["id", "other"]

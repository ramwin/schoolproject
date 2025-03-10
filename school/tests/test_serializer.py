#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import logging
import pydash
from school.serializers import DictModelSerializer

from django.test import TestCase


LOGGER = logging.getLogger(__name__)


class Test(TestCase):

    def test(self):
        origin_data = {
                "other": {
                    "pop_out_attribute": "required",
                    "integer": "1",
                    "keep_attribute": "optional",
                }
        }
        serializer = DictModelSerializer(data=origin_data)
        serializer.is_valid(raise_exception=True)

        formated_data = serializer.validated_data
        LOGGER.info("formated_data: %s", formated_data)
        LOGGER.info("origin_data: %s", origin_data)
        LOGGER.info("formated_data: %s", formated_data)
        LOGGER.info("origin_data: %s", origin_data)
        
        self.assertNotEqual(
                formated_data,
                origin_data,
        )
        origin_data["other"]["integer"] = 1
        self.assertEqual(
                formated_data,
                origin_data,
        )

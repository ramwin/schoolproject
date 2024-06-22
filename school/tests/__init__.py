import logging

from django.test import TestCase, override_settings
from django_redis import get_redis_connection

from school.consts import REDIS
from school.serializers import AliasSerializer


LOGGER = logging.getLogger(__name__)


@override_settings(CACHES={
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://localhost:6379/7",
    }
})
class TestSummary(TestCase):
    def test_redis_db(self):
        redis: Redis = get_redis_connection("default")
        self.assertEqual(
                redis.connection_pool.connection_kwargs["db"],
                7,
        )
        self.assertEqual(
                REDIS.connection_pool.connection_kwargs["db"],
                7,
        )


class TestLog(TestCase):

    def test(self):
        LOGGER.info("info")
        LOGGER.warning("warning")
        LOGGER.error("error")


class TestGender(TestCase):

    def test(self):
        data_cn = {
                "性别": "男",
        }
        data_en = {
                "male": "0",
        }
        serializer = AliasSerializer(data=data_cn)
        self.assertFalse(serializer.is_valid(), serializer.errors)
        serializer = AliasSerializer(data=data_en)
        self.assertFalse(serializer.is_valid())

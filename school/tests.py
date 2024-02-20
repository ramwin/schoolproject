from django.test import TestCase, override_settings
from django_redis import get_redis_connection


# Create your tests here.

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
                redis.client_info()["db"],
                7,
        )

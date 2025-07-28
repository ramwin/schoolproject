#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


from redis.asyncio.cluster import RedisCluster as AsyncRedisCluster


ASYNC_REDIS_CLUSTER = AsyncRedisCluster(host="localhost", port=7000)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


from django_redis import get_redis_connection



# 这个有很大的隐患，因为test的时候返回的时已经初始化了的。
REDIS = get_redis_connection("default")

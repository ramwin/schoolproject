#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


from .settings import CONFIG


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        "NAME": "schoolproject",
        "max_size": 5,
        "CONN_MAX_AGE": 10,
        "PASSWORD": CONFIG["password"],
        "OPTIONS": {
            # "pool": True,
        },
    },
    "db_02": {
        'ENGINE': 'django.db.backends.postgresql',
        "NAME": "schoolproject_02",
        "PASSWORD": CONFIG["password"],
    },
}

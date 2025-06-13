#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import logging
import os
import sys
from pathlib import Path


class NoErrorFilter(logging.Filter):

    def filter(self, record):
        if record.levelname == "ERROR":
            return False
        return True


BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / 'log'
LOG_DIR.mkdir(exist_ok=True)

for level in ["debug", "info", "warning", "error"]:
    LOG_DIR.joinpath(level).mkdir(exist_ok=True)


DEFAULT_HANDLERS = [
        'debug_file',
        'info_file',
        'warning_file',
        'error_file',
        "console",
        "error_console",
]
handlers = {
    'error_file': {
        'level': "ERROR",
        'class': 'logging_ext2.handlers.TimedRotatingFileHandler',
        'max_keep': 100,
        'filename': LOG_DIR / "error" / 'error.log',
        'formatter': 'verbose',
        "datetime_formatter": "%Y-%m-%d",
    },
    'warning_file': {
        'level': "WARNING",
        'class': 'logging.handlers.RotatingFileHandler',
        'filename': LOG_DIR / "warning" / 'warning.log',
        'maxBytes': 1024 * 1024 * 10,
        'backupCount': 20,
        'formatter': 'verbose',
    },
    'info_file': {
        'level': "INFO",
        'class': 'logging_ext2.handlers.TimedRotatingFileHandler',
        'max_keep': 100,
        'filename': LOG_DIR / "info" / 'info.log',
        'formatter': 'verbose',
        "datetime_formatter": "%Y-%m-%d_%H",
    },
    'debug_file': {
        'level': "DEBUG",
        'class': 'logging_ext2.handlers.TimedRotatingFileHandler',
        'max_keep': 100,
        'filename': LOG_DIR / "debug" / 'debug.log',
        "datetime_formatter": "%Y-%m-%d_%H",
        'formatter': 'verbose',
    },
    'console': {
        'class': 'colorlog.StreamHandler',
        'level': "INFO",
        'formatter': 'color',
        'stream': sys.stdout,
        "filters": ["no_error"],
    },
    'error_console': {
        'class': 'colorlog.StreamHandler',
        'level': "ERROR",
        'formatter': 'color',
        'stream': sys.stderr,
    },
}
loggers = {
    'default': {
        'handlers': DEFAULT_HANDLERS,
        'level': "INFO",
        "propagate": False,
    },
    'django': {
        'handlers': DEFAULT_HANDLERS,
        'level': "INFO",
        "propagate": False,
    },
    'testapp': {
        'handlers': DEFAULT_HANDLERS,
        'level': "INFO",
        "propagate": False,
    },
    # 各个APP配置
    'django_commands': { 'handlers': DEFAULT_HANDLERS, 'level': "INFO", "propagate": False },
    'school': { 'handlers': DEFAULT_HANDLERS, 'level': "INFO", "propagate": False },
    'schoolproject': { 'handlers': DEFAULT_HANDLERS, 'level': "INFO", "propagate": False },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    "filters": {
        "no_error": {
            "()": NoErrorFilter,
        },
    },
    'formatters': {
        'verbose': {
            'format': ('[%(levelname)5s] %(asctime)s %(process)d %(name)s '
                       '%(funcName)s (line: %(lineno)d)'
                       '    %(message)s'),
        },
        'color': {
            '()': 'colorlog.ColoredFormatter',
            'format': ('%(log_color)s[%(levelname)5s] %(asctime)s %(process)d %(name)s '
                       '%(funcName)s (line: %(lineno)d)'
                       '    %(message)s'),
        },
        'simple': {
            'format': '[%(levelname)s] %(module)s:%(lineno)d %(message)s ',
        },
    },
    'handlers': handlers,
    'loggers': loggers,
}

if sys.argv[0] == 'manage.py':
    (LOG_DIR / sys.argv[1]).mkdir(exist_ok=True, parents=True)
    DEFAULT_HANDLERS.append("command_file")
    handlers["command_file"] = {
        'level': "INFO",
        'class': 'logging.handlers.TimedRotatingFileHandler',
        'when': 'h',
        'backupCount': 100,
        'filename': LOG_DIR / sys.argv[1] / 'info.log',
        'formatter': 'verbose',
    }

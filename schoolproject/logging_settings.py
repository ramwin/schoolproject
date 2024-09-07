#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import os
import sys

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / 'log'
LOG_DIR.mkdir(exist_ok=True)
(LOG_DIR / sys.argv[1]).mkdir(exist_ok=True, parents=True)

DEFAULT_HANDLERS = [
        'debug_file', 'info_file',
        'warning_file', 'error_file',
        "console",
        'command_file',
]
handlers = {
    'error_file': {
        'level': "ERROR",
        'class': 'logging.FileHandler',
        'filename': LOG_DIR / 'error.log',
        'formatter': 'verbose',
    },
    'warning_file': {
        'level': "WARNING",
        'class': 'logging.handlers.RotatingFileHandler',
        'filename': LOG_DIR / 'warning.log',
        'maxBytes': 1024 * 1024 * 10,
        'backupCount': 20,
        'formatter': 'verbose',
    },
    'info_file': {
        'level': "INFO",
        'class': 'logging.handlers.RotatingFileHandler',
        'maxBytes': 1024 * 1024 * 10,
        'backupCount': 20,
        'filename': LOG_DIR / 'info.log',
        'formatter': 'verbose',
    },
    'command_file': {
        'level': "INFO",
        'class': 'logging.handlers.RotatingFileHandler',
        'maxBytes': 1024 * 1024 * 10,
        'backupCount': 20,
        'filename': LOG_DIR / sys.argv[1] / 'info.log',
        'formatter': 'verbose',
    },
    'debug_file': {
        'level': "DEBUG",
        'class': 'logging.handlers.RotatingFileHandler',
        'maxBytes': 1024 * 1024 * 10,
        'backupCount': 20,
        'filename': LOG_DIR / 'debug.log',
        'formatter': 'verbose',
    },
}
if os.environ.get("TERM") == "xterm-256color":
    handlers['console'] = {
        'class': 'colorlog.StreamHandler',
        'level': "INFO",
        'formatter': 'color',
        'stream': sys.stdout,
    }
else:
    handlers['console'] = {
        'class': 'logging.StreamHandler',
        'formatter': 'verbose',
        'stream': sys.stdout,
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
}
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
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

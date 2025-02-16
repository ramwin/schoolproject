#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


from pathlib import Path


if Path.cwd().name == "schoolproject":
    from school.models.base import *
    from school.models.relations import *
    from school.utils import *

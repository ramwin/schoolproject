#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


from school.models.base import Tag
from school.models.inherit import (
        Animal,
        Dog,
        )


def run():
    dog = Dog.objects.create(name='1', tag=Tag.objects.create())
    dog.tag.save(using='db_02')
    dog.save(using='db_02')
    animal = Animal.objects.get()
    dog = Dog.objects.get()
    # dog删除时,animal也会被删除
    # dog.delete()
    # assert Animal.objects.exists() == False
    dog.delete(keep_parents=True)
    assert Animal.objects.exists() == True

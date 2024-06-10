#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


from school import utils


def test_get_int(monkeypatch):

    def mockreturn():
        return 1

    monkeypatch.setattr(utils, "get_int", mockreturn)

    a = utils.get_int()
    assert a == 1

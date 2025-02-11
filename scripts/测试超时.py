#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from multiprocessing import Pool
import requests


def call(timeout):
    res = requests.get(f'http://localhost:8000/sleep/{timeout}/', timeout=10)
    res.raise_for_status()

with Pool(10) as p:
    p.map(call, range(10))

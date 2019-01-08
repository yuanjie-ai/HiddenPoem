#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '__main__'
__author__ = 'JieYuan'
__mtime__ = '19-1-8'
"""
import fire
from .poetry_gen import PoetryGen


def gen(**kwargs):
    result = PoetryGen(False).gen(**kwargs)
    for idx in range(0, len(result), 8):
        print('\033[94m%s\033[0m' % result[idx] + result[idx + 1: idx + 7])


if __name__ == '__main__':
    fire.Fire(gen)

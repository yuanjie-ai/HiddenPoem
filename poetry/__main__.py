#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
__title__ = '__main__'
__author__ = 'JieYuan'
__mtime__ = '19-1-8'
"""
import fire
from .poetry_gen import PoetryGen

gen = PoetryGen.gen


if __name__ == '__main__':
    fire.Fire()
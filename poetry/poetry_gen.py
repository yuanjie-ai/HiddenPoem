#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'poetry_gen.py'
__author__ = 'JieYuan'
__mtime__ = '19-1-7'
"""

import torch
from .poetry_model import PoetryModel
from . import gen_acrostic
from .data import get_data
from .config import Config

opt = Config()

data, word2ix, ix2word = get_data(opt)
model = PoetryModel(len(word2ix), 128, 256)
print(model)
map_location = lambda s, l: s
state_dict = torch.load(opt.model_path, map_location=map_location)
model.load_state_dict(state_dict)


class PoetryGen(object):

    def __init__(self, color_print=True):
        self.color_print = color_print

    def gen(self, **kwargs):
        for i in kwargs.items():
            setattr(opt, *i)
        start_words = opt.start_words.replace(',', '，').replace('.', '。').replace('?', '？').replace('!', '！')
        result = gen_acrostic(opt, model, start_words, ix2word, word2ix, opt.prefix_words)
        result = '\n'.join([result[idx: idx + 7] for idx in range(0, len(result), 7)])
        if self.color_print:
            for idx in range(0, len(result), 8):
                print('\033[94m%s\033[0m' % result[idx] + result[idx + 1: idx + 7])
        else:
            return result


if __name__ == '__main__':
    PoetryGen.gen({'start_words': '简历投过来'})

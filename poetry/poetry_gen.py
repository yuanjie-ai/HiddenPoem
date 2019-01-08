#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'main'
__author__ = 'JieYuan'
__mtime__ = '19-1-7'
"""

import torch
from .poetry_model import PoetryModel
from ..poetry import gen_acrostic
from .data import get_data
from .config import Config

opt = Config()


class PoetryGen(object):
    @staticmethod
    def gen(**kwargs):
        for i in kwargs.items():
            setattr(opt, *i)
        data, word2ix, ix2word = get_data(opt)
        model = PoetryModel(len(word2ix), 128, 256)
        # print(model)
        map_location = lambda s, l: s
        state_dict = torch.load(opt.model_path, map_location=map_location)
        model.load_state_dict(state_dict)
        start_words = opt.start_words.replace(',', '，').replace('.', '。').replace('?', '？').replace('!', '！')
        result = gen_acrostic(opt, model, start_words, ix2word, word2ix, opt.prefix_words)

        return '\n'.join([result[idx: idx + 7] for idx in range(0, len(result), 7)])


if __name__ == '__main__':
    PoetryGen.gen({'start_words': '简历投过来小米欢迎你'})

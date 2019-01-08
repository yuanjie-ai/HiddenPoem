#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '__init__.py'
__author__ = 'JieYuan'
__mtime__ = '19-1-7'
"""
import numpy as np
import torch
from .poetry_gen import PoetryGen
__chars = {237,
         320,
         565,
         569,
         1115,
         1548,
         1592,
         1727,
         2205,
         2509,
         2707,
         2862,
         3057,
         3224,
         3257,
         3302,
         3357,
         3435,
         3450,
         3653,
         4160,
         4546,
         4637,
         4697,
         5008,
         5250,
         5380,
         5423,
         6025,
         6110,
         6542,
         7057,
         7066,
         7360,
         7435,
         8290,
         8291,
         8292}


def gen_acrostic(opt, model, start_words, ix2word, word2ix, prefix_words=None):
    """
    生成藏头诗
    start_words : u'深度学习'
    生成：
    深木通中岳，青苔半日脂。
    度山分地险，逆浪到南巴。
    学道兵犹毒，当时燕不移。
    习根通古岸，开镜出清羸。
    """
    results = ''
    start_word_len = len(start_words)
    input = (torch.Tensor([word2ix['<START>']]).view(1, 1).long())

    hidden = None

    index = 0  # 用来指示已经生成了多少句藏头诗

    if prefix_words:
        for word in prefix_words:
            output, hidden = model(input, hidden)
            input = (input.data.new([word2ix[word]])).view(1, 1)

    for i in range(opt.max_gen_len):
        output, hidden = model(input, hidden)
        top_indexs = output.data[0].topk(40)[1].numpy()
        for top_index in top_indexs:
            if top_index not in __chars:
                break

        w = ix2word[top_index]

        # if (pre_word in {'。', '！', '？', '<START>'}):  # '，'
        # 如果遇到句号，藏头的词送进去生成
        if i % 7 == 0:
            if index == start_word_len:
                # 如果生成的诗歌已经包含全部藏头的词，则结束
                break
            else:
                # 把藏头的词作为输入送入模型
                w = start_words[index]
                index += 1
                # input = (input.data.new([word2ix[w]])).view(1, 1)
                input = (input.data.new([word2ix.get(w, np.random.randint(0, 8000))])).view(1, 1)
        else:
            # 否则的话，把上一次预测是词作为下一个词输入
            input = (input.data.new([word2ix[w]])).view(1, 1)

        results += w if i % 7 else w
        # results.append(w if i % 7 else '\n'+w)
    return results


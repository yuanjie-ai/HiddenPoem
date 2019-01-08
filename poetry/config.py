#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'config'
__author__ = 'JieYuan'
__mtime__ = '19-1-7'
"""
import os

get_module_path = lambda path, file=__file__: os.path.normpath(os.path.join(os.getcwd(), os.path.dirname(file), path))


class Config(object):
    lr = 1e-3
    weight_decay = 1e-4
    epoch = 20
    batch_size = 128
    maxlen = 125  # 超过这个长度的之后字被丢弃，小于这个长度的在前面补空格

    data_path = get_module_path('./checkpoints/')  # 诗歌的文本文件存放路径
    pickle_path = get_module_path('./checkpoints/tang.npz')  # 预处理好的二进制文件
    author = None  # 只学习某位作者的诗歌
    constrain = None  # 长度限制
    category = 'poet.tang'  # 类别，唐诗还是宋诗歌(poet.song)
    model_path = get_module_path('./checkpoints/tang_w.pth')  # 预训练模型路径
    prefix_words = "爆竹声中一岁除，春风送暖入屠苏。"  # 不是诗歌的组成部分，用来控制生成诗歌的意境
    start_words = '闲云潭影日悠悠'  # 诗歌开始
    acrostic = False  # 是否是藏头诗
    model_prefix = 'checkpoints/w'  # 模型保存路径
    max_gen_len = 256

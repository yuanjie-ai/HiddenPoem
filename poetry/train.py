#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'train'
__author__ = 'JieYuan'
__mtime__ = '19-1-7'
"""
import torch
from torch import nn
from torch.utils.data import DataLoader

from tqdm import tqdm
from .poetry_model import PoetryModel
from .data import get_data
from .config import Config

opt = Config()


def train(**kwargs):
    for k, v in kwargs.items():
        setattr(opt, k, v)

    # 获取数据
    data, word2ix, ix2word = get_data(opt)
    data = torch.from_numpy(data)
    dataloader = DataLoader(data, batch_size=opt.batch_size, shuffle=True, num_workers=1)

    # 模型定义
    model = PoetryModel(len(word2ix), 128, 256)
    optimizer = torch.optim.Adam(model.parameters(), lr=opt.lr)
    criterion = nn.CrossEntropyLoss()
    if opt.model_path:
        model.load_state_dict(torch.load(opt.model_path))

    for epoch in range(opt.epoch):
        for ii, data_ in tqdm(enumerate(dataloader)):
            # 训练
            data_ = data_.long().transpose(1, 0).contiguous()
            optimizer.zero_grad()
            input_, target = data_[:-1, :], data_[1:, :]
            output, _ = model(input_)
            loss = criterion(output, target.view(-1))
            loss.backward()
            optimizer.step()

        torch.save(model.state_dict(), '%s_%s.pth' % (opt.model_prefix, epoch))


if __name__ == '__main__':
    train()

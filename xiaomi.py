# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'main'
__author__ = 'JieYuan'
__mtime__ = '19-1-8'
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-


import socket

socket.SO_REUSEPORT = 15

import re
from datetime import datetime
from vibora import Vibora, Response, Request
from vibora.responses import JsonResponse
from urllib import parse
from poetry.poetry_gen import PoetryGen
import numpy as np
import random
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict

chinese = re.compile('[^\u4e00-\u9fa5]+')

p = PoetryGen(False)

get_unique = lambda iterable: list(OrderedDict.fromkeys(list(iterable)))


def get_poetry(corpus, zishu=7):
    url = "http://www.shicimingju.com/cangtoushi/index.html"
    text = requests.get(url, {'kw': corpus, 'zishu': zishu}, timeout=1).text
    soup = BeautifulSoup(text, 'lxml')
    l = list(map(lambda x: x.text.split(), soup.find_all('div', class_='cangtoushi-item')))
    if l:
        np.random.shuffle(l)
        return l[0]


app = Vibora()


@app.route('/poetry/getpoem/<corpus>', methods=['GET'])
async def page(corpus: str):
    rst = {}
    rst['time'] = str(datetime.now())
    corpus = parse.unquote(corpus)
    corpus = chinese.sub('', corpus)
    corpus_unique = get_unique(corpus)
    try:
        if 2 < len(corpus) < 13 and len(corpus_unique) > 2:
            # 判断重复字
            if len(set(corpus)) < len(corpus):
                idxs = set(range(len(corpus))) - set(np.unique(list(corpus), True)[1])  # 重复字索引
                poem = get_poetry(''.join(corpus_unique))

                if poem:
                    for idx in idxs:
                        poem.insert(idx, p.gen(start_words=corpus[idx]).split())
                else:
                    poem = p.gen(start_words=corpus).split()

                rst['poem'] = poem
                rst['warning'] = '含重复字: 模型作诗'
            else:
                poem = get_poetry(corpus)
                rst['poem'] = poem if poem else p.gen(start_words=corpus).split()
                rst['warning'] = '无重复字: 原诗优先'
        else:
            rst['poem'] = p.gen(start_words=corpus).split()
            rst['warning'] = '字数不足: 模型作诗'

    except Exception as e:
        rst['poem'] = p.gen(start_words=corpus).split()
        rst['warning'] = str(e)
    finally:
        return JsonResponse([rst])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, workers=4, verbose=False)

# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'main'
__author__ = 'JieYuan'
__mtime__ = '19-1-8'
"""
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

chars = '神圣贤文武成康献懿元章僖釐景宣明昭正敬恭庄肃穆戴翼襄烈桓威勇毅克庄圉御魏安定简贞节白匡质靖真顺思考皓显和元高光大英睿博宪坚孝忠惠德仁智慎礼义周敏信达宽理凯清直钦益良度类基慈齐深温让密厚纯勤谦友祁广淑俭灵荣厉比絜舒贲逸退讷偲逑懋宜哲察通仪经庇协端休悦绰容确恒熙洽绍世果太'
chinese = re.compile('[^\u4e00-\u9fa5]+')

p = PoetryGen(False)


def get_poetry(corpus):
    url = "http://www.shicimingju.com/cangtoushi/index.html"
    text = requests.get(url, {'kw': corpus, 'zishu': 7}).text
    soup = BeautifulSoup(text, 'lxml')
    l = list(map(lambda x: x.text.split(), soup.find_all('div', class_='cangtoushi-item')))
    np.random.shuffle(l)
    return chinese.sub(random.sample(chars, 1), l[0])


app = Vibora()


@app.route('/poetry/getpoem/<corpus>', methods=['GET'])
async def page(corpus: str):
    rst = {}
    rst['time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    corpus = parse.unquote(corpus)
    corpus = chinese.sub('', corpus)

    if 1 < len(corpus) < 13:
        if len(set(corpus[:6])) < 6:
            rst['poem'] = p.gen(start_words=corpus).split()
        else:
            try:
                rst['poem'] = get_poetry(corpus[:6]) + p.gen(start_words=corpus[6:]).split()
            except Exception as e:
                print(e)
                rst['poem'] = p.gen(start_words=corpus).split()
        rst['warning'] = ''
    else:
        rst['poem'] = ''
        rst['warning'] = 'chinese-length not in (1, 13)'
    return JsonResponse([rst])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, workers=4, verbose=False)

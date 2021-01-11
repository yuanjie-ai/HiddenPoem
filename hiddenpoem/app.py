#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : Python.
# @File         : poetry
# @Time         : 2020-01-09 12:53
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :

"""
1. 去重
2. 结果为空字符串
3. 含有非中文字符

"""
from meutils.pipe import *
from fastapi import FastAPI

get_file_path = lambda path, file: \
    os.path.normpath(os.path.join(os.getcwd(), os.path.dirname(file), path))

data_cache = Path(get_file_path("./data_cache", __file__))

reg_chinese = re.compile('[^\u4e00-\u9fa5]+')


def get_poem_map(file='./cangtoushi7.txt'):
    df = pd.read_csv(file, '\t', names=['char', 'poems'])
    return dict(zip(df.char, df.poems.str.split()))


poem7 = {
    **get_poem_map(data_cache / 'poem_ext.txt'),
    **get_poem_map(data_cache / 'cangtoushi7.txt')
}
poem5 = get_poem_map(data_cache / 'cangtoushi5.txt')

new_chars = list('好闪高神强嗨迷靓甜纯萌恒酷美靓真帅纯柔惠慧雅倩秀亲')


def poem_gen(sent):
    r = []
    for char in sent:
        poems = poem7.get(char) or poem5.get(char)
        unique_poems = list(set(poems) - set(r))
        if unique_poems:
            poem = np.random.choice(unique_poems)
            poem = (poem + poem[-1] * 3)[:7]
        else:
            poem = char + "".join(np.random.choice(new_chars, 6))
        r.append(reg_chinese.sub(np.random.choice(new_chars), poem))
    return r


app = FastAPI()


@app.get("/{title}")
async def read_item(title):
    title = reg_chinese.sub('', title)
    return {"title": title, "poem": poem_gen(title)}


if __name__ == '__main__':
    import os
    import socket

    me = socket.gethostname() == 'yuanjie-Mac.local'
    gunicorn = "gunicorn" if me else "/opt/soft/python3/bin/gunicorn"

    main_file = __file__.split('/')[-1].split('.')[0]
    os.system(f"{gunicorn} -c gun.py {main_file}:app")

# gunicorn main:app -b 0.0.0.0:8000  -w 4 -k uvicorn.workers.UvicornH11Worker --daemon

import requests
from bs4 import BeautifulSoup
url = "http://www.shicimingju.com/cangtoushi/index.html"
text = requests.get(url, {'kw': '小米浏览器猪年快乐', 'zishu': 7}).text

soup = BeautifulSoup(text, 'lxml')
l = list(map(lambda x: x.text.split(), soup.find_all('div', class_='cangtoushi-item')))
import numpy as np
np.random.shuffle(l)
l[0]

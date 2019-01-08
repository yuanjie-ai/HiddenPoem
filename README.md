- **Install**
```python
pip install git+https://github.com/Jie-Yuan/pytorch-poetry.git
```
- **Shell**
```
python -m poetry --start_words '小米春节藏头诗'
```

- **Python**
```python
from poetry.poetry_gen import PoetryGen
print(PoetryGen().gen(start_words='小米春节藏头诗'))
```
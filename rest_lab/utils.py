import json
import random
from datetime import datetime
from pathlib import Path


def big_file():
    with open(Path('rest_lab/bigdata.json')) as f:
        return f.read()


def fib(n=32):

    def f(n):
        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            return f(n-1)+f(n-2)

    print('FIB')
    return f(n)


def simple():
    print('SIMPLE')
    return {"message": "ok"}


def big_data():

    def stream():
        data = BIG_DATA.encode()
        pos = 0
        chunk_size = len(data) // 10
        payload = data[pos: pos + chunk_size]
        while payload:
            yield payload
            pos += chunk_size + 1
            payload = data[pos: pos + chunk_size]

    print('BIG')
    return stream()


BIG_DATA = big_file()

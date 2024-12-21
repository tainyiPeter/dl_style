

import hashlib
from utility import *
from hl_public import *

def up(dict, key, value):
    if (values := dict.get(key)) is None:
        dict[key] = values = []
    if value not in values:
        values.append(value)

def t1(str):
    try:
        km = int(str)
    except ValueError:
        return 0

    print("ook")
    return km
if __name__ == '__main__':
    dict = {
        "a": [1]
    }

    k = t1("3333")

    print(k)

    print("hello")
    pass








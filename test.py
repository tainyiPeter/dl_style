

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
    dictGood = {

        "6": [42,3],
        "7": [6],
        "8": [8]
    }

    for idx, value in dictGood.items():
        for i in value:
            print("idx:", idx, " value:", i)
    pass








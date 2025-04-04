

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

def GetDirs(path_k):
    if not os.path.exists(path_k):
        return []
    paths = os.walk(path_k)
    dirs = []
    for path, dir_lst, file_lst in paths:
        # print("dir_cnt:", len(dir_lst))
        # print("file_cnt:", len(file_lst))
        for dir_name in dir_lst:
            f = os.path.join(path, dir_name)
            mydict = {}
            mydict["name"] = dir_name
            mydict["fullname"] = f
            dirs.append(mydict)
        return dirs

def GetTranIndex(strName):
    tranName = "transition"
    l = strName.split("_")
    strIndex = l[1]
    tranFlag = l[2]
    if(tranFlag != tranName):
        return 0
    try:
        tranIndex = int(strIndex)
    except ValueError:
        return 0
    return tranIndex

if __name__ == '__main__':
    # dictGood = {
    #
    #     "6": [42,3],
    #     "7": [6],
    #     "8": [8]
    # }
    #
    # for idx, value in dictGood.items():
    #     for i in value:
    #         print("idx:", idx, " value:", i)
    # srcList = []
    # for fileIdx, dirName in enumerate(srcList):
    #     print(f"idx:{fileIdx}, name:{dirName}")

    # path = "D:\\work\\liuzf\\test\\video\\third\\chaoxianshi"
    # srcList = GetDirs(path)
    # for fileIdx, dirName in enumerate(srcList):
    #     print(f"idx:{fileIdx}, name:{dirName}")

    scopeType = 1
    TranIndex = GetTranIndex("menghuan_54_transition")
    styleType = 5
    TranIndex += 100 * styleType
    TranIndex = TranIndex + 1000 * scopeType

    print(TranIndex)
    pass








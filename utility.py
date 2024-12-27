
import os
import json

def is_nan(str):
    try:
        f = float(str)
        return f != f
    except ValueError:
        return False
def GetDirs(path_k):
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

def GetFiles(path_k):
    paths = os.walk(path_k)
    files = []
    for path, dir_lst, file_lst in paths:
        # print("dir_cnt:", len(dir_lst))
        # print("file_cnt:", len(file_lst))
        for dir_name in file_lst:
            f = os.path.join(path, dir_name)
            files.append(f)
        return files
    return files

def SaveDictFile(strFileName, c):
    dstPath = os.path.dirname(strFileName)
    if not os.path.exists(dstPath):
        os.makedirs(dstPath)  # 创建路径
    strJson = json.dumps(c)
    with open(strFileName, "w", encoding='utf-8') as file:
        # print(strJson)
        file.write(strJson)
    pass

def CheckAndCreatePath(dstPath):
    if not os.path.exists(dstPath):
        os.makedirs(dstPath)  # 创建路径
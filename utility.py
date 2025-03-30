
import os
import json
import hashlib

def is_nan(str):
    try:
        f = float(str)
        return f != f
    except ValueError:
        return False
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

def calculate_file_sha256(file_path):
    """
    计算文件的SHA-256哈希值。
    :param file_path: 文件路径
    :return: 文件的SHA-256哈希值
    """
    sha256 = hashlib.sha256()

    with open(file_path, 'rb') as file:
        while True:
            data = file.read(65536)
            if not data:
                break
            sha256.update(data)

    return sha256.hexdigest()
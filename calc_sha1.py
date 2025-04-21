from openpyxl import Workbook
import pandas as pd
import os
import hashlib
from datetime import datetime

def SaveDataToExcel(fileName, data):
    # print(data)
    # for key, val in enumerate(data.items()):
    #     print("key:", val[0], " value:", val[1])
    with pd.ExcelWriter(fileName) as writer:
        for key, val in enumerate(data.items()):
            # print("val0:", val[0])
            # print("val1:", val[1])
            df = pd.DataFrame(val[1])
            df.to_excel(writer, sheet_name=val[0], index=False)

# def DaveData(fileName, sheet)
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

def calculate_file_sha1(file_path):
    sha1 = hashlib.sha1()

    with open(file_path, 'rb') as file:
        while True:
            data = file.read(65536)
            if not data:
                break
            sha1.update(data)

    return sha1.hexdigest()

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

def getLastFile(strFullName):
    val_array = strFullName.split("\\")
    cnt = len(val_array)
    if cnt <= 2:
        print ("getLastFile cnt failed:", cnt)
        return ""

    return val_array[cnt-2]

#     pass
if __name__ == "__main__":
    data2 = {
        'Column1': [1, 2, 3],
        'Column2': ['A', 'B', 'C']
    }

    # langPath = "D:\\work\\dexuan\\2501\\play_test\\dstPath_123"
    # dst = "D:\\tmp\\12"

    langPath = "D:\\work\\stella\\play_short_20250404_finish\\dstPath"
    # dst = "D:\\work\\jiachaoyi\\4-19"

    # dict_lang = {
    #     "fileName":[],
    #     "sha1":[]
    # }

    # stylePath = "D:\\work\\stella\\01-15\\test\\dst"
    # stylePath = "D:\\work\\liuzf\\test\\dst"
    parentPath = "D:\\work\\stella\\2025-04-02\\test"
    parentPath += "\\dst"

    current_time = datetime.now().strftime("_%Y-%m-%d_%H-%M-%S")
    dstFile = f"{parentPath}\\cloud_sha256{current_time}.xlsx"

    dirs = GetDirs(parentPath)
    langdict = {
        "name": "lang",
        "fullname": langPath
    }
    dirs.append(langdict)

    dict = {}
    for pathKey, pathValue in enumerate(dirs):
        # print("pathvalue:", pathValue["fullname"])
        files = GetFiles(pathValue["fullname"])
        fileList = []
        shaList = []
        style_name = ""
        for key, val in enumerate(files):
            # print("val:", val)
            fileName = os.path.basename(val)
            style_name = getLastFile(val)
            sha1_value = calculate_file_sha256(val)

            # print(f"style_name:{style_name}, type:{type(style_name)}")

            fileList.append(fileName)
            shaList.append(sha1_value)
        a = {
            "fileName": fileList,
            "sha256": shaList
        }
        print(f"style name:{style_name}")
        dict[style_name] = a

    SaveDataToExcel(dstFile, dict)
    print(f"finish dstFile:{dstFile}")
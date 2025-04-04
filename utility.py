
import os
import json
import hashlib
from pathlib import Path

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
    print(f"save file:{strFileName}")

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

# 包含扩展名
def check_file_exists_pathlib(folder_path, filename):
    """
    使用pathlib检查文件是否存在
    :param folder_path: 文件夹路径
    :param filename: 要查找的文件名
    :return: 存在返回True，否则返回False
    """
    file_path = Path(folder_path) / filename
    return file_path.is_file()

# 不含扩展名
def find_file_without_extension(folder_path, filename_without_ext):
    """
    查找文件夹中是否存在指定名称的文件（不包含扩展名）

    :param folder_path: 要搜索的文件夹路径
    :param filename_without_ext: 要查找的文件名（不含扩展名）
    :return: 如果找到返回True，否则返回False
    """
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            name, ext = os.path.splitext(file)
            if name == filename_without_ext:
                return True
    return False

# 不区分大小写
def find_file_ignore_case(folder_path, filename_without_ext):
    """
    查找文件夹中是否存在指定名称的文件（不含扩展名且不区分大小写）

    :param folder_path: 要搜索的文件夹路径
    :param filename_without_ext: 要查找的文件名（不含扩展名）
    :return: 如果找到返回True，否则返回False
    """
    target = filename_without_ext.lower()  # 转换为小写用于比较
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            name, ext = os.path.splitext(file)
            if name.lower() == target:
                return True
    return False


def change_specific_extensions(folder_path, old_extension, new_extension):
    """
    只修改特定扩展名的文件
    :param folder_path: 文件夹路径
    :param old_extension: 原扩展名（如 '.jpg'）
    :param new_extension: 新扩展名（如 '.png'）
    :return: 修改的文件数量
    """
    count = 0
    for filename in os.listdir(folder_path):
        if filename.endswith(old_extension):
            old_path = os.path.join(folder_path, filename)

            # 替换扩展名
            new_filename = filename[:-len(old_extension)] + new_extension
            new_path = os.path.join(folder_path, new_filename)

            os.rename(old_path, new_path)
            count += 1

    return count


def find_files_containing_name_pathlib(folder_path, search_name):
    """
    使用pathlib查找包含特定名称的文件
    :param folder_path: 文件夹路径
    :param search_name: 要查找的名称片段
    :return: 匹配的文件路径列表
    """
    folder = Path(folder_path)
    search_lower = search_name.lower()
    return [str(file) for file in folder.iterdir()
            if file.is_file() and search_lower in file.name.lower()]

def find_file_containing_ignore_case(folder_path, file_name):
    """
    查找文件夹中是否存在指定名称的文件（不含扩展名且不区分大小写）

    :param folder_path: 要搜索的文件夹路径
    :param filename_without_ext: 要查找的文件名（不含扩展名）
    :return: 如果找到返回True，否则返回False
    """
    target = file_name.lower()  # 转换为小写用于比较
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            name, ext = os.path.splitext(file)
            # name += "."
            low_name = name.lower()
            if target in name.lower():
                return name + ext
    return ""

def discard_end_char(s):
    l = ['.', "!", "?", ' ', '  ']
    s = s.strip()
    for c in l:
        if c in s:
            last_dot_index = s.rfind(c)
            s_len = len(s)
            if(s_len == last_dot_index+len(c)):
                s = s[0:last_dot_index]
    return s
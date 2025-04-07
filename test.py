

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

def InvalidRow(rowName):
    pos = rowName.find("wukong_nodamage")
    return pos != -1

if __name__ == '__main__':
    rowName = "wukong_nodamage_end1"
    ret = InvalidRow(rowName)
    print(f"ret:{ret}")
    # audioSrcPath = "D:\\work\\dexuan\\2501\\play_test\\audio_short\\希腊语"
    # slogan = "Δεν έχει σημασία. Η αποτυχία είναι σαν ένα αεράκι το καλοκαίρι: φεύγει γρήγορα"
    # slogan = discard_end_char(slogan)
    # audioFileName = find_file_containing_ignore_case(audioSrcPath, slogan)
    # print(f"ret:{audioFileName}")

    # s = "Блискавична перемога! Неймовірний рух!  "
    #
    # s = discard_end_char(s)
    # # if '.' in s:
    # #     last_dot_index = s.rfind('.')
    # #     s_len = len(s)
    # #     if(s_len == last_dot_index+1):
    # #         s = s[0:last_dot_index]
    # print(s)  # 输出: example.file.nametxt

    pass








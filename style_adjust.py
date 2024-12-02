import sys
import os
import shutil
import re


def FetchDigit(txt):
    digit_list = re.findall(r'\d+', txt)

    for digit in digit_list:
        return digit

    return 0
def GetFiles(path_k):
    paths = os.walk(path_k)
    files = []
    for path, dir_lst, file_lst in paths:
        print("dir_cnt:", len(dir_lst))
        print("file_cnt:", len(file_lst))
        for dir_name in file_lst:
            f = os.path.join(path, dir_name)
            files.append(f)
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

def proc_rename_num(s):
    srcDirs = GetDirs(s)
    idx = 1
    while idx < 26:
        word = "(" + str(idx) + ")"
        for i, val in enumerate(srcDirs):
            if word in val["name"]:
                print(val["fullname"])
                os.rename(val["fullname"], s + "\\" + str(idx))
                break

        idx = idx + 1
def mymovefile(srcfile, dstpath):  # 移动函数
    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))
    else:
        fpath, fname = os.path.split(srcfile)  # 分离文件名和路径
        if not os.path.exists(dstpath):
            os.makedirs(dstpath)  # 创建路径
        shutil.move(srcfile, dstpath + fname)  # 移动文件
        print("movfile: ", srcfile,  "====>", dstpath + fname)


def move_file_to_dst_by_keyword(src_path, word, dst_path):
    dst_bgm = dst_path + "\\" + "BGM\\"
    if not os.path.exists(dst_bgm):
        os.makedirs(dst_bgm)  # 创建路径

    for filename in os.listdir(src_path):
        fp = os.path.join(src_path, filename)
        if os.path.isfile(fp) and word in filename:
            bgm_file = dst_bgm + word + ".webm"
            shutil.move(fp, bgm_file)
def proc_video(s, d):
    # 创建目标文件夹
    #os.makedirs(d)

    srcFiles = GetDirs(s)
    for i, val in enumerate(srcFiles):

        dst_i = d + "\\" + val["name"]

        move_file_to_dst_by_keyword(val["fullname"], "begin", dst_i)
        move_file_to_dst_by_keyword(val["fullname"], "end", dst_i)

        dst_i_effect = dst_i + "\\effects\\"
        effFiles = GetFiles(val["fullname"])
        for i_eff, val_eff in enumerate(effFiles):
            mymovefile(val_eff, dst_i_effect)

def proc_video_in_file(srcFile, dstFile):
    if not os.path.exists(srcFile):
        print("srcFile not exit:", srcFile)
        return

    if not os.path.exists(dstFile):
        os.makedirs(dstFile)  # 创建路径

    move_file_to_dst_by_keyword(srcFile, "begin", dstFile)
    move_file_to_dst_by_keyword(srcFile, "end", dstFile)

    dst_i_effect = dstFile + "\\effects\\"
    effFiles = GetFiles(srcFile)
    for i_eff, val_eff in enumerate(effFiles):
        mymovefile(val_eff, dst_i_effect)


def move_file(src, dst, style, bVideo):
    if(len(src) == 0 or len(dst) == 0):
        print("input valid path")
        return

def proc_video_first(src, dst):
    if not os.path.exists(dst):
        os.makedirs(dst)  # 创建路径

    style_list = [
        "chaoxianshi",
        "erciyuan",
        "gaoran",
        "guichu",
        "menghuan",
    ]

    for i, styleName in enumerate(style_list):
        srcDir = src + "\\" + styleName
        dstDir = dst + "\\" + styleName

        srcList = GetDirs(srcDir)
        for fileIdx, dirName in enumerate(srcList):
            subName = dirName["name"]
            digit = FetchDigit(subName)
            if(int(digit) == 0):
                print("------------------------------------------------------------------------------------")
                print("invalid file:", subName)
                continue

            srcFullFile = srcDir + "\\" + subName
            dstFullFile = dstDir + "\\" + digit

            print("full src:", srcFullFile)
            print("full dst:", dstFullFile)

            proc_video_in_file(srcFullFile, dstFullFile)
    pass

def proc_video_second(src, dst):
    if not os.path.exists(dst):
        os.makedirs(dst)  # 创建路径

    style_list = [
        "chaoxianshi",
        "erciyuan",
        "gaoran",
        "guichu",
        "menghuan",
        "fugu",
        "jike",
    ]

    for i, styleName in enumerate(style_list):
        srcDir = src + "\\" + styleName
        dstDir = dst + "\\" + styleName

        index = 25
        if (styleName == "fugu" or styleName == "jike") :
            index = 0

        srcList = GetDirs(srcDir)
        for fileIdx, dirName in enumerate(srcList):
            subName = dirName["name"]
            digit = FetchDigit(subName)
            if(int(digit) == 0):
                print("------------------------------------------------------------------------------------")
                print("invalid file:", subName)
                continue

            srcFullFile = srcDir + "\\" + subName
            dstFullFile = dstDir + "\\" + str(int(digit) + index)

            print("full src:", srcFullFile)
            print("full dst:", dstFullFile)

            proc_video_in_file(srcFullFile, dstFullFile)
    pass

def proc_audio_in_file(srcDir, dstDir, dstName, idx):
    files = GetFiles(srcDir)
    for idx, val in enumerate(files):
        srcFileName = os.path.basename(val)
        strNum = FetchDigit(srcFileName)
        nNum = int(strNum) + idx
        dstNumDir = dstDir + "\\" + str(nNum)

        dstFullName = dstNumDir + "\\BGM\\"
        if not os.path.exists(dstFullName):
            os.makedirs(dstFullName)  # 创建路径
        dstFullName += dstName

        print("src:", val)
        print("dst:", dstFullName)
        shutil.copy(val, dstFullName)

    pass

def proc_audio_first(src, dst):
    srcStyleList = GetDirs(src)

    for fileIdx, dirName in enumerate(srcStyleList):
        subName = dirName["name"]
        subFullName = dirName["fullname"]
        srcNumList = GetDirs(subFullName)
        for numIdx, numName in enumerate(srcNumList):
            subNumName = numName["name"]
            subNumFullName = numName["fullname"]
            strM1 = subNumFullName + "\\BGM\\m1.aac"
            strM2 = subNumFullName + "\\BGM\\m2.aac"
            strS30 = subNumFullName + "\\BGM\\s30.aac"

            dstDir = dst + "\\" + subName + "\\" + subNumName + "\\BGM"
            if not os.path.exists(dstDir):
                os.makedirs(dstDir)  # 创建路径

            print("src:", strM1)
            print("dst:", dstDir)



    pass
def proc_audio_second(src, dst):
    if not os.path.exists(dst):
        os.makedirs(dst)  # 创建路径

    style_list = [
        "chaoxianshi",
        "erciyuan",
        "gaoran",
        "guichu",
        "menghuan",
        "fugu",
        "jike",
    ]

    for i, styleName in enumerate(style_list):
        srcDir = src + "\\" + styleName
        dstDir = dst + "\\" + styleName

        index = 25
        if (styleName == "fugu" or styleName == "jike") :
            index = 0

        srcList = GetDirs(srcDir)
        for fileIdx, dirName in enumerate(srcList):
            subName = dirName["name"]
            dstName = ""
            if(subName == "30s"):
                dstName = "s30.aac"
            elif(subName == "60s"):
                dstName = "m1.aac"
            else:
                dstName = "m2.aac"

            srcFiles = srcDir + "\\" + subName
            proc_audio_in_file(srcFiles, dstDir, dstName, index)
    pass

if __name__ == '__main__':
    dst = "D:\\work\\dexuan\\2501\\dst"

    # 处理视频
    src_video_first = "D:\\work\\dexuan\\2501\\video\\first"
    src_video_second = "D:\\work\\dexuan\\2501\\video\\second"
    proc_video_first(src_video_first, dst)
    proc_video_second(src_video_second, dst)

    # 处理音频
    src_audio_first = "D:\\work\\dexuan\\2501\\audio\\first"
    src_audio_second = "D:\\work\\dexuan\\2501\\audio\\second"
    proc_audio_first(src_audio_first, dst)
    proc_audio_second(src_audio_second, dst)

    print("finish")









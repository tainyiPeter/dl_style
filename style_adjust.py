import sys
import os
import shutil
import re
from pathlib import Path

def FetchDigit(txt):
    digit_list = re.findall(r'\d+', txt)

    for digit in digit_list:
        return digit

    return 0

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


# 移动到bgm目录
def move_file_to_dst_by_keyword(src_path, word, dst_path):
    dst_bgm = dst_path + "\\" + "BGM\\"
    if not os.path.exists(dst_bgm):
        os.makedirs(dst_bgm)  # 创建路径

    for filename in os.listdir(src_path):
        fp = os.path.join(src_path, filename)
        if os.path.isfile(fp) and word in filename:
            bgm_file = dst_bgm + word + ".webm"
            shutil.move(fp, bgm_file)

# 移动到转场目录
def move_file_to_tran_by_keyword(src_path, word, dst_path):
    dst_bgm = dst_path + "\\" + "trans\\"
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
    move_file_to_tran_by_keyword(srcFile, "transition", dstFile)

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


def proc_video_third(src, dst):
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

        # index = 25
        # if (styleName == "fugu" or styleName == "jike") :
        #     index = 0

        srcList = GetDirs(srcDir)
        for fileIdx, dirName in enumerate(srcList):
            subName = dirName["name"]
            digit = FetchDigit(subName)
            if(int(digit) == 0):
                print("------------------------------------------------------------------------------------")
                print("invalid file:", subName)
                continue

            srcFullFile = srcDir + "\\" + subName
            dstFullFile = dstDir + "\\" + str(int(digit))

            print("full src:", srcFullFile)
            print("full dst:", dstFullFile)

            proc_video_in_file(srcFullFile, dstFullFile)
    pass

def proc_audio_in_file(srcDir, dstDir, dstName, idx):
    print("proc_audio_in_file src", srcDir, "dst:", dstDir, "idx:", idx)
    files = GetFiles(srcDir)
    for i, val in enumerate(files):
        srcFileName = os.path.basename(val)
        strNum = FetchDigit(srcFileName)
        nNum = int(strNum) + idx
        dstNumDir = dstDir + "\\" + str(nNum)

        print("[test] num:", nNum, " idx:", idx, " dstNumDir:", dstNumDir)

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

    print("proc_audio_first, src:", src, "dst:", dst)
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
            shutil.copy(strM1, dstDir)
            shutil.copy(strM2, dstDir)
            shutil.copy(strS30, dstDir)
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


def get_audio_src_path(audio_path, c, style, idx):
    cnt = c.get(style, 0)
    if cnt == 0:
        print(f"sss:{audio_path}, {style}, {idx}")
    idx = (idx % cnt) + 1
    fullpath = audio_path + "\\" + str(idx)

    return fullpath

def get_one_audio(c, style, idx):
    styleDict = c.get(style)
    if(styleDict is None):
        print(f"get one audio failed, {style}")
        return 0
    cnt = len(styleDict)
    idx = (idx % cnt) + 1
    return idx

# D_JiKe_2_1min.aac -> m1.aac
# D_JiKe_2_2min.aac -> m2.aac
# D_JiKe_2_30s.aac -> s30.aac
def convertName(fileName):
    # acclist = fileName.split("_")
    # if(len(acclist) != 4):
    #     return ""
    # if(acclist[3] == "1min.aac"):
    #     return "m1.aac"
    # elif(acclist[3] == "2min.aac"):
    #     return "m2.aac"
    # elif(acclist[3] == "30s.aac"):
    #     return "s30.aac"
    # else:
    #     return ""

    if "1min" in fileName:
        return "m1.aac"
    elif "2min" in fileName:
        return "m2.aac"
    elif "30s" in fileName:
        return "s30.aac"
    else:
        return ""
    pass

# A_GaoRan_2_2min.aac
def AppendAudioToDict(c, fullName):
    fileName = os.path.basename(fullName)
    nameList = fileName.split("_")
    if(len(nameList) != 4):
        print(f"AppendAudio filed, {fileName}")
        return
    styleName = nameList[1]
    styleName = styleName.lower()
    idx = nameList[2]
    name = nameList[3]
    styleDic = c.get(styleName, {})
    # print(f"type:", type(styleDic))
    audioList = styleDic.get(idx, [])
    audioList.append(fileName)
    styleDic[idx] = audioList
    # print(audioList)
    c[styleName] = styleDic



def proc_audio_third(src, dst):
    # prepare
    if not os.path.exists(dst):
        os.makedirs(dst)  # 创建路径

    print(f"proc audio third {src}, {dst}")
    batchRename(src, "ChaoXieShi", "chaoxianshi")

    style_list = [
        "chaoxianshi",
        "erciyuan",
        "gaoran",
        "guichu",
        "menghuan",
        "fugu",
        "jike",
    ]

    print(f"src path:{src}")
    print(f"dst path:{dst}")

    # c = {}
    # srcAudioList = GetDirs(src)
    # for fileIdx, pathName in enumerate(srcAudioList):
    #     fileName = pathName["name"]
    #     fullName = pathName["fullname"]
    #     cnt = 0
    #     if not os.path.exists(fullName):
    #         cnt = 0
    #     else:
    #         cnt = sum(os.path.isdir(os.path.join(fullName, name)) for name in os.listdir(fullName))
    #
    #     c[fileName] = cnt
    # print(c)

    d = {}
    files = GetFiles(src)
    for f in files:
        # print(f"file:{f}")
        AppendAudioToDict(d, f)
    print(d)

    for i, styleName in enumerate(style_list):
        dstDir = dst + "\\" + styleName
        dstList = GetDirs(dstDir)
        idx = 0
        for fileIdx, dirName in enumerate(dstList):
            dstFullPath = dirName["fullname"]
            dstFullPath += "\\BGM"
            # audio_path = get_audio_src_path(srcDir, c, styleName, idx)
            audio_idx = get_one_audio(d, styleName, idx)
            if(audio_idx == 0):
                print(f"audio_idx is o, {styleName}, {idx}")
                continue
            #print(f"src:{src}, styleName:{styleName}, idx:{idx}, audio_idx:{audio_idx}, dstFullPath:{dstFullPath}")
            audio_style = d.get(styleName)
            if(audio_style is None):
                print(f"audio style is none , {styleName}")
                continue
            audio_aac = audio_style.get(str(audio_idx))
            if(audio_aac is None):
                print(f"audio acc is none, {audio_idx}, {styleName}")
                continue
            for accName in audio_aac:
                newAccName = convertName(accName)
                if(len(newAccName) == 0):
                    print(f"newAccName is empty, {accName}")
                    continue
                srcFullName = src + "\\" + accName
                dstFullName = dstFullPath + "\\" + newAccName
                print(f"audio copy: {srcFullName} -> {dstFullName}")
                shutil.copy(srcFullName, dstFullName)
            idx += 1

def showAllFiles(strPath, type):
    #print("showAllFiles:", strPath)
    files = GetFiles(strPath)
    cnt = len(files)
    if(cnt == 0):
        print("showAllFiles no files, failed", strPath)
        # return
    for i, val in enumerate(files):
        fileName = os.path.basename(val)
        # print("fileName:", fileName)

    if(type == 1):  # bgm
        if(cnt != 5):
            print("show all bgm file failed:", strPath, "type:", type, " cnt:", cnt)
    elif(type == 2): # effect
        if (cnt < 2):
            print("show all effect file failed:", strPath, "type:", type, " cnt:", cnt)
    elif(type == 3): # effect
        if (cnt < 1):
            print("show all tran file failed:", strPath, "type:", type, " cnt:", cnt)
    pass
def checkDst(dst):
    dstDirs = GetDirs(dst)
    for i, val in enumerate(dstDirs):
        # print("style full name:", val["fullname"])
        numDirs = GetDirs(val["fullname"])
        for iNum, valNum in enumerate(numDirs):
            # print("num full name:", valNum["fullname"])
            bgmPath = valNum["fullname"] + "\\BGM"
            effPath = valNum["fullname"] + "\\effects"
            tranPath = valNum["fullname"] + "\\trans"
            showAllFiles(bgmPath, 1)
            showAllFiles(effPath,2)
            showAllFiles(tranPath, 3)
    pass

def batchRename(path, oldName, newName):
    files = GetFiles(path)
    for f in files:
        if oldName in f:
            new_file = f.replace(oldName, newName)
            oldFullName = f
            newFullName = new_file
            print(f"{oldFullName} -> {newFullName}")
            shutil.move(oldFullName, newFullName)

if __name__ == '__main__':
    # parentPath = "D:\\work\\dexuan\\2501\\1209-test"
    # parentPath = "D:\\work\\stella\\01-15\\test"

    # parentPath = "D:\\work\\liuzf\\test"
    # dst = parentPath + "\\dst"

    # D:\work\stella\2025-04-02\test
    parentPath = "D:\\work\\stella\\2025-04-02\\test"
    dst = parentPath + "\\dst"

    # 处理视频
    # src_video_first = parentPath + "\\video\\first"
    # proc_video_first(src_video_first, dst)
    # src_video_second = parentPath + "\\video\\second"
    # proc_video_second(src_video_second, dst)
    # src_video_third = parentPath + "\\video\\third"
    # proc_video_third(src_video_third, dst)
    # #
    # # # 处理音频
    # src_audio_first = parentPath + "\\audio\\first"
    # proc_audio_first(src_audio_first, dst)
    # src_audio_second = parentPath + "\\audio\\second"
    # proc_audio_second(src_audio_second, dst)
    # src_audio_third = parentPath + "\\audio\\third"
    # proc_audio_third(src_audio_third, dst)

    checkDst(dst)
    print("finish style adjust")

# srcfile 需要复制、移动的文件
# dstpath 目的地址

import os
import shutil
from glob import glob


def mycopyfile(srcfile, dstpath):  # 复制函数
    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))
    else:
        fpath, fname = os.path.split(srcfile)  # 分离文件名和路径
        if not os.path.exists(dstpath):
            os.makedirs(dstpath)  # 创建路径
        shutil.copy(srcfile, dstpath + fname)  # 复制文件
        print("copy %s -> %s" % (srcfile, dstpath + fname))


def mymovefile(srcfile, dstpath):  # 移动函数
    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))
    else:
        fpath, fname = os.path.split(srcfile)  # 分离文件名和路径
        if not os.path.exists(dstpath):
            os.makedirs(dstpath)  # 创建路径
        shutil.move(srcfile, dstpath + fname)  # 移动文件
        print("movfile: ", srcfile,  "====>", dstpath + fname)

# src_dir = './'
# dst_dir = './copy/'  # 目的路径记得加斜杠
# src_file_list = glob(src_dir + '*')  # glob获得路径下所有文件，可根据需要修改
# for srcfile in src_file_list:
#     mycopyfile(srcfile, dst_dir)  # 复制文件



def move_file_to_dst_by_keyword(src_path, word, dst_path):
    dst_bgm = dst_path + "\\" + "BGM\\"
    if not os.path.exists(dst_bgm):
        os.makedirs(dst_bgm)  # 创建路径

    for filename in os.listdir(src_path):
        fp = os.path.join(src_path, filename)
        if os.path.isfile(fp) and word in filename:
            bgm_file = dst_bgm + word + ".webm"
            shutil.move(fp, bgm_file)

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

# print("aa:", dstfile)


#dstfile = search("D:/tmp/8-4/menghuan", "begi", dst_dir)




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

        #print("fiel:", val["name"])
        #os.makedirs(dst_bgm)
        #print("序号：%s   值：%s" % (i + 1, val))


def proc_audio(s, d):
    srcDirs = GetDirs(s)
    print("proc_audio:", s)
    for i, val in enumerate(srcDirs):
            srcFiles = GetFiles(val["fullname"])
            #print(srcFiles)

            idx = 1
            while idx < 26:
                findit = False
                word = "_" + str(idx)
                for i_file, val_files in enumerate(srcFiles):
                    if word in val_files:
                        dst_file = d + "\\" + str(idx) + "\\BGM\\"
                        if val["name"] == "1min":
                            dst_file = dst_file + "m1.aac"
                        elif val["name"] == "2min":
                            dst_file = dst_file + "m2.aac"
                        elif val["name"] == "30s":
                            dst_file = dst_file + "s30.aac"
                        print(val_files, "->>", dst_file)
                        shutil.move(val_files, dst_file)
                        print("audio :", val_files, "---->", dst_file)
                        findit = True
                        break
                    #print("error audio:", word, "find it :", findit)
                idx = idx + 1

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


# 1 文件夹修改
src_dir_chaoxianshi = "d:/tmp/src/chaoxianshi"
src_dir_erciyuan = "d:/tmp/src/erciyuan"
src_dir_gaoran = "d:/tmp/src/gaoran"
src_dir_guichu = "d:/tmp/src/guichu"
src_dir_menghuan = "d:/tmp/src/menghuan"

print("1")

# 2
chaoxianshi_video = src_dir_chaoxianshi + "\\video"
chaoxianshi_audio = src_dir_chaoxianshi + "\\audio"
chaoxianshi_dst = "D:/tmp/dst/chaoxianshi"

proc_rename_num(chaoxianshi_video)
proc_video(chaoxianshi_video, chaoxianshi_dst)
proc_audio(chaoxianshi_audio, chaoxianshi_dst)

print("2-1")

erciyuan_video = src_dir_erciyuan + "\\video"
erciyuan_audio = src_dir_erciyuan + "\\audio"
erciyuan_dst = "D:/tmp/dst/erciyuan"
proc_rename_num(erciyuan_video)
proc_video(erciyuan_video, erciyuan_dst)
proc_audio(erciyuan_audio, erciyuan_dst)
print("2-2")

gaoran_video = src_dir_gaoran + "\\video"
gaoran_audio = src_dir_gaoran + "\\audio"
gaoran_dst = "D:/tmp/dst/gaoran"
proc_rename_num(gaoran_video)
proc_video(gaoran_video, gaoran_dst)
proc_audio(gaoran_audio, gaoran_dst)
print("2-3")

guichu_video = src_dir_guichu + "\\video"
guichu_audio = src_dir_guichu + "\\audio"
guichu_dst = "D:/tmp/dst/guichu"
proc_rename_num(guichu_video)
proc_video(guichu_video, guichu_dst)
proc_audio(guichu_audio, guichu_dst)
print("2-4")

menghuan_video = src_dir_menghuan + "\\video"
menghuan_audio = src_dir_menghuan + "\\audio"
menghuan_dst = "D:/tmp/dst/menghuan"
proc_rename_num(menghuan_video)
proc_video(menghuan_video, menghuan_dst)
proc_audio(menghuan_audio, menghuan_dst)
print("2-5")

print("finish")

# proc_rename_num("D:\\tmp\\guichu")
# proc_video(src_dir_video, dst_dir)
# proc_audio(src_dir_audio, dst_dir)

#dowork(src_dir, dst_dir)

    #if os.path.isfile(fp) and word in filename:


# mycopyfile("D:\\tmp\\src\\menghuan\\menghuan (4)\\menghuan 04_begin_ok.webm", "d:\\tmp\\111\\222\\1.BMP")

#shutil.copyfile(child_file, result_file)
#shutil.move("D:\\tmp\\a.webm","d:\\tmp\\kk\\b.webm")

#shutil.move("d:\\tmp\\b.webm","d:\\tmp\\kk\\b.webm")






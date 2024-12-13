import zipfile
import os


def zip_folder(folder_path, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_in_zip_path = os.path.relpath(file_path, os.path.dirname(folder_path))
                zipf.write(file_path, file_in_zip_path)


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


def zip_all_files(dir):
    dirs = GetDirs(dir)
    for i, val in enumerate(dirs):
        val_zip = val["fullname"] + ".zip"
        print("before zip path:", val["fullname"], " after zip:", val_zip, " i:", i)
        zip_folder(val["fullname"], val_zip)
        remove_folder(val["fullname"])

    import os


def remove_folder(path):
    if os.path.exists(path):
        if os.path.isfile(path) or os.path.islink(path):
            os.remove(path)
        else:
            for filename in os.listdir(path):
                remove_folder(os.path.join(path, filename))
            os.rmdir(path)


if __name__ == '__main__':
    # dst = "D:\\work\\dexuan\\2501\\dst"
    dst = "D:\\tmp\\dst"
    styles = GetDirs(dst)
    for i, val in enumerate(styles):
        zip_all_files(val["fullname"])
        print("style fullname:", val["fullname"])

# zip_all_files("D:\\tmp22\\dst\\chaoxianshi")
# zip_all_files("D:\\tmp22\\dst\\erciyuan")
# zip_all_files("D:\\tmp22\\dst\\gaoran")
# zip_all_files("D:\\tmp22\\dst\\guichu")
# zip_all_files("D:\\tmp22\\dst\\menghuan")

print("finish")

# 使用函数压缩指定文件夹
# folder_to_compress = 'D:\\tmp\\style\\2'  # 要压缩的文件夹路径
# zip_file_output = 'D:\\tmp\\style\\2.zip'  # 输出的.zip文件名
# zip_folder(folder_to_compress, zip_file_output)
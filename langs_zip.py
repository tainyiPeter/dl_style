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

def unzip_file(zip_file, dstPath):
    if not os.path.exists(dstPath):
        os.makedirs(dstPath)  # 创建路径

    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(dstPath)

if __name__ == '__main__':
    # dst = "D:\\work\\dexuan\\2501\\dst"
    src = "D:\\work\\dexuan\\2501\\play_test\\dstPath_123"
    src = "D:\\work\\stella\\play_short_20250404_finish\\dstPath"


    zip_all_files(src)

    # langs = GetFiles(src)
    # cnt = 0
    # for key, val in enumerate(langs):
    #     unzip_file(val, dst)
    #     cnt += 1
    #     print("unzip file:", val, " cnt:", cnt)


    print("finish")


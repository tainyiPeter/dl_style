import shutil

import json

import hashlib



c = {}
def test():
    c1 = {}
    c1["a"] = 1
    c1["b"] = 2

    return c1


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

if __name__ == '__main__':
    # 假设有一个名为data.json的文件
    json_file_path = 'D:\\tmp\\kr.zip'

    sha256 = calculate_file_sha256(json_file_path)

    print(sha256)







import shutil

import json



c = {}
def test():
    c1 = {}
    c1["a"] = 1
    c1["b"] = 2

    return c1

if __name__ == '__main__':
    # 假设有一个名为data.json的文件
    json_file_path = 'D:\\tmp\\styleFile\\beb_scope.json'

    # 读取并解析JSON文件
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 现在data变量包含了JSON文件中的数据，可以按需使用
    print("cnt:", len(data))
    print(data["7"])





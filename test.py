import shutil

if __name__ == '__main__':
    # LangtoColumn = {
    #     "German": [4, "yun"],
    #     "33" : [5, "3"],
    #     "44": [5, "7"]
    # }
    #
    # for i, (lang, value) in enumerate(LangtoColumn.items()):
    #     if(lang == "33"):
    #         continue
    #     print("lang:", lang, " key", value[0], " value:", value[1])
    # print("hello")
    #
    # shutil.move("d:\\tmp\\1.txt", "d:\\tmp2\\33.txt")

    num = 33
    width = 8
    str_num = f"{num-30:0>2}.aac"  # 使用0填充，宽度为6
    print(str_num)  # 输出: '000123'

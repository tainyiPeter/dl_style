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

    src = "D:\\tmp\\play\\法语\\2sds.aac"
    dst = "D:\\tmp\\play\\20.aac"

    try:
        for i in range(0, 10):
            print("befor i:", i)
            shutil.move(src, dst)
            print("i:", i)

    except:
        print("sss")


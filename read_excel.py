import os

import os, re
import os.path as path
import pandas as pd
import shutil
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

def resize(filename):
    wb = load_workbook(filename)
    for sheet in wb.sheetnames:
        ws = wb[sheet]
        df = pd.read_excel(filename, sheet).fillna('-')
        df.loc[len(df)] = list(df.columns)
        for col in df.columns:
            index = list(df.columns).index(col)
            letter = get_column_letter(index + 1)
            collen = df[col].apply(lambda x: len(str(x).encode())).max()
            ws.column_dimensions[letter].width = collen * 1 + 4
    wb.save(filename)

def findFile(pattern, base='.'):
    regex = re.compile(pattern)
    matches = []
    for root, dirs, files in os.walk(base):
        for f in files:
            if regex.match(f):
                matches.append(path.join(root, f))
    return matches

def procData(excelFile, langDstPath, audioSrcPath, column):
    print("excelFile:", excelFile, " langDstPath:", langDstPath, " audioSrcPath:", audioSrcPath, " column:", column)

    if not os.path.exists(langDstPath):
        os.makedirs(langDstPath)  # 创建路径

    # slogan
    sloganPath = langDstPath + "\\slogan"
    if not os.path.exists(sloganPath):
        os.makedirs(sloganPath)  # 创建路径
    killSloganPath = sloganPath + "\\kill"
    deadSloganPath = sloganPath + "\\dead"
    if not os.path.exists(killSloganPath):
        os.makedirs(killSloganPath)  # 创建路径
    if not os.path.exists(deadSloganPath):
        os.makedirs(deadSloganPath)  # 创建路径

    killSloganFile = killSloganPath + "\\" + "slogan.dat"
    deadSloganFile = deadSloganPath + "\\" + "slogan.dat"

    # audio
    audioPath = langDstPath + "\\audio"
    if not os.path.exists(audioPath):
        os.makedirs(audioPath)  # 创建路径
    killAudioPath = audioPath + "\\kill"
    deadAudioPath = audioPath + "\\dead"
    if not os.path.exists(killAudioPath):
        os.makedirs(killAudioPath)  # 创建路径
    if not os.path.exists(deadAudioPath):
        os.makedirs(deadAudioPath)  # 创建路径

    df = pd.read_excel(excelFile)
    pageSize = 20
    with open(killSloganFile, "w", encoding='utf-8') as kf:
        killIdx = 1
        for i in range(killIdx, killIdx+pageSize):
            slogan = str(df.iloc[i, column])
            #
            audioFileName = slogan+".aac"
            audioFiles = findFile(audioFileName, audioSrcPath)
            if(len(audioFiles) == 0):
                print("find kill audio file, failed:", audioFileName)
                continue
            num_acc = f"{i:0>2}.aac"
            shutil.move(audioSrcPath + "\\" + audioFileName, killAudioPath + "\\" + num_acc)  #
            slogan += "\n"
            kf.write(slogan)

    with open(deadSloganFile, "w", encoding='utf-8') as deadSloganFile:
        deadIdx = 22
        for i in range(deadIdx, deadIdx + pageSize):
            #print("i:", i, "column:", column)
            slogan = str(df.iloc[i, column])
            audioFileName = slogan + ".aac"
            audioFiles = findFile(audioFileName, audioSrcPath)
            if(len(audioFiles) == 0):
                print("find dead audio file, failed:", audioFileName)
                continue
            num_acc = f"{i-deadIdx-1:0>2}.aac"
            shutil.move(audioSrcPath + "\\" + audioFileName, deadAudioPath + "\\" + num_acc)  #
            slogan += "\n"
            deadSloganFile.write(slogan)

    pass
def GetCellData(fileName, row, column):
    #fileName = "D:\\work\\dexuan\\2501\\play_2501.xlsx"
    df = pd.read_excel(fileName)
    cell_data = df.iloc[row, column]  # 读取第row行，第column列的数据
    return cell_data

# test append string
def appendString(fileName, info):
    with open(fileName, "w") as file:
        file.write(info)
        file.write("\n")
        file.write("33333")
        file.write("\n")
        file.write("4444")
        file.write("\n")

def ExcelToLangFile(excelFile, dstPath, audioPath, column):
    if not os.path.exists(dstPath):
        os.makedirs(dstPath)  # 创建路径

    procData(excelFile, dstPath, audioPath, column)
    pass




if __name__ == '__main__':
    playDst = "D:\\work\\dexuan\\2501\\play111\\"

    excelFile = playDst + "play_2501.xlsx"
    audioPath = playDst + "audio"
    dstPath = playDst + "dstPath"

    #test
    #procData(fileName, "d:\\tmp\\kill.txt", "d:\\tmp\\dead.txt", 6)
    #data = GetCellData(fileName, 13, 3)
    #print("data:", data)

    LangtoColumn = {
        # "cn": 2,
        # "en": 3,
        "German": [4, "德语"],
        "French": [5, "法语"],
        "Polish": [6, "波兰语"],
        "Jap": [7, "日本语"],
        "Span": [8, "西班牙语"],
        "Itali": [9, "意大利语"],
        "Arabic": [10, "阿拉伯语"],
        "CnTradition": [11, "繁体中文"],
        "PortugueseBrazil": [12, "巴西葡萄牙语"],
        "Korean": [13, "韩语"],
        "Norwegian": [14, "挪威语"],
        "Hung": [15, "匈牙利语"],
        "Czech": [16, "捷克语"],
        "Slovak": [17, "斯洛伐克语"],
        "Romanian": [18, "罗马尼亚语"],
        "Dutch": [19, "荷兰语"],
        "Swedish": [20, "瑞典语"],
        "Croatian": [21, "克罗地亚语"],
        "Finnish": [22, "芬兰语"],
        "Turkish": [23, "土耳其语"],
        "Ukra": [24, "乌克兰语"],
        "Danish": [25, "丹麦语"],
        "PortugueseEurope": [26, "葡萄牙语"],
        "Greek": [27, "希腊语"],
        "Russian": [28, "俄语"],
    }

    for i, (lang, value) in enumerate(LangtoColumn.items()):
        audioLangPath = audioPath + "\\" + value[1]
        langDstPath = dstPath + "\\" + lang
        print("lang:", lang, " col:", value[0], " audioFile:", audioLangPath, " langDstPath:", langDstPath)
        procData(excelFile, langDstPath, audioLangPath, value[0])


    ## test
    # files = findFile("Guter Treffer\\w.aac", audioPath+"\\deyu")
    # print("path:", audioPath+"\\deyu")
    # print("cnt:", len(files))


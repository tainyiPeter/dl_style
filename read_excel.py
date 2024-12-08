import os

import time
import datetime
import pandas as pd
import json
import sys
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from copy import copy

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

def procData(fileName, killFile, deadFile, column):
    df = pd.read_excel(fileName)
    pageSize = 20
    with open(killFile, "w", encoding='utf-8') as kf:
        killIdx = 1
        for i in range(killIdx, killIdx+pageSize):
            slogan = str(df.iloc[i, column]) + "\n"
            kf.write(slogan)

            #print(i)
    #df1 = pd.read_excel(fileName)
    with open(deadFile, "w", encoding='utf-8') as deadFile:
        deadIdx = 22
        for i in range(deadIdx, deadIdx + pageSize):
            #print("i:", i, "column:", column)
            slogan = str(df.iloc[i, column]) + "\n"
            deadFile.write(slogan)

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

def ExcelToLangFile(excelFile, dstPath, column):
    if not os.path.exists(dstPath):
        os.makedirs(dstPath)  # 创建路径
    killFile = dstPath + "\\" + "kill.txt"
    deadFile = dstPath + "\\" + "dead.txt"
    procData(excelFile, killFile, deadFile, column)
    pass


if __name__ == '__main__':
    fileName = "D:\\work\\dexuan\\2501\\play_2501.xlsx"

    #test
    #procData(fileName, "d:\\tmp\\kill.txt", "d:\\tmp\\dead.txt", 6)
    #data = GetCellData(fileName, 13, 3)
    #print("data:", data)

    dstPath = "D:\\work\\dexuan\\2501\\play"
    LangtoColumn = {
        "cn": 2,
        "en": 3,
        "German": 4,
        "French": 5,
        "Polish": 6,
        "Jap":7,
        "Span":8,
        "Itali":9,
        "Arabic":10,
        "CnTradition":11,
        "PortugueseBrazil":12,
        "Korean":13,
        "Norwegian":14,
        "Hung":15,
        "Czech":16,
        "Slovak":17,
        "Romanian":18,
        "Dutch":19,
        "Swedish":20,
        "Croatian":21,
        "Finnish":22,
        "Turkish":23,
        "Ukra":24,
        "Danish":25,
        "PortugueseEurope":26,
        "Greek":27,
        "Russian":28,
    }

    for i, (lang, col) in enumerate(LangtoColumn.items()):
        # print("key:", i)
        print("lang:", lang, "col", col)

        langPath = dstPath + "\\" + lang
        ExcelToLangFile(fileName, langPath, col)
    pass


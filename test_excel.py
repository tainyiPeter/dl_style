from utility import *
from hl_public import *

import pandas as pd
from datetime import datetime

def test(fileName):
    # 定义两个字典
    data1 = {
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'City': ['New York', 'San Francisco', 'Los Angeles']
    }

    data2 = {
        'Product': ['Apple', 'Banana', 'Orange'],
        'Price': [1.2, 0.5, 0.8],
        'Quantity': [10, 20, 15]
    }

    # 将字典转换为 DataFrame
    df1 = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)

    # 使用 ExcelWriter 写入多个工作表
    with pd.ExcelWriter(fileName) as writer:
        df1.to_excel(writer, sheet_name='Sheet1', index=False)
        df2.to_excel(writer, sheet_name='Sheet2', index=False)

    print(f"数据已写入：{fileName}")

def TestMulSheet(fileName, mulData):
    with pd.ExcelWriter(fileName) as writer:
        idx = 0
        for data in mulData:
            print(data)
            idx += 1
            pageName = f"page_{idx}"
            df = pd.DataFrame(data)
            df.to_excel(writer, sheet_name=pageName, index=False)

def SaveMulsheetToExcel(fileName, mulData):
    with pd.ExcelWriter(fileName) as writer:
        for key, data in mulData.items():
            df = pd.DataFrame(data)
            df.to_excel(writer, sheet_name=key, index=False)

if __name__ == '__main__':
    #dst = "d:\\tmp\\16.xlsx"

    dst = "d:\\tmp"
    current_time = datetime.now().strftime("lz_uf_%Y-%m-%d_%H-%M-%S")
    dstFile = f"{dst}\\{current_time}.xlsx"

    # 定义两个字典
    data1 = {
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'City': ['New York', 'San Francisco', 'Los Angeles']
    }

    data2 = {
        'Product': ['Apple', 'Banana', 'Orange'],
        'Price': [1.2, 0.5, 0.8],
        'Quantity': [10, 20, 15]
    }

    mulData = {}
    mulData["apple"] = data1
    mulData["prduct"] = data2

    # for key, value in mulData.items():
    #     print(f"Key: {key}, Value: {value}")

    SaveMulsheetToExcel(dstFile, mulData)

    # TestMulSheet(dst, "page1", data1)
    # TestMulSheet(dst, "page2", data2)

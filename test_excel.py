from utility import *
from hl_public import *

import pandas as pd

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


if __name__ == '__main__':
    dst = "d:\\tmp\\12.xlsx"
    test(dst)

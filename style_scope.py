import os
import shutil
import json
import pandas as pd

from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

def int_to_bool(num):
    if num == 0:
        return False
    else:
        return True
def GetGameType(strType):
    gameStringToType = {
        "LOL": 1,
        "DOTA2": 2,
        "CROSSFIRE": 3,
        "PUBG": 4,
        "WORLD_OF_TANKS": 5,
        "CS2": 6,
        "NARAKA": 7,
        "APEX": 8,
        "FORTNITE": 9,
        "WORLD_OF_WARSHIPS": 10,
        "all": 100
    }
    strType = strType.strip()
    if(strType not in gameStringToType):
        print("get game type failed,", strType)
        return 0
    else:
        return gameStringToType[strType]

def GetGameEvent(strEvent):
    gameEventToInt = {
        "kill":0,
        "assist":2,
        "konck down":3,
        "defeat":4,
        "victory":5
    }

    if(strEvent not in gameEventToInt):
        print("get game event failed,", strEvent)
        return -1
    else:
        return gameEventToInt[strEvent]
# 1
def updateEvent(events, gameEvent, styleIndex):
    if(gameEvent not in events):
        events[gameEvent] = []
    events[gameEvent].append(styleIndex)

#def appendEvent(events, gameEvent, idx):


# 第二步
def updateGame(games, strGameType, bSelected, events):
    gameType = GetGameType(strGameType)
    if(gameType not in games):
        games["type"] = gameType
    # games["prop"] = prop
    games["scope"] = int_to_bool(bSelected)
    games["event"] = events


##
def updateStyle(styles, styleType, games):
    if(styleType not in styles):
        styles[styleType] = {}
    styles[styleType] = games

def GetStyleIndex(strName, bSecond):
    # print("---------strName：", strName)
    l = strName.split("_")
    styleName = l[0]
    strIndex = l[1]
    styleIndex = int(strIndex)
    if((bSecond == True) and (styleName != "fugu") and (styleName != "jike")):
        styleIndex += 25

    return styleIndex

def AppendStyle(collect, styleType, strGameType, gameEvent, bSelected, strStyle, bSecond):
    styleIdx = GetStyleIndex(strStyle, bSecond)

    if( styleType not in collect):
        collect[styleType] = {}

    eventName = "event"
    if(eventName not in collect[styleType]):
        collect[styleType][eventName] = {}

    # events = styleData["event"]
    updateEvent(collect[styleType][eventName], gameEvent, styleIdx)  #
    updateGame(collect[styleType], strGameType, bSelected, collect[styleType][eventName])
    updateStyle(collect, styleType, collect[styleType])

    pass

def SaveLocalData(dstPath, jsonData):
    if not os.path.exists(dstPath):
        os.makedirs(dstPath)  # 创建路径

    for key, value in enumerate(jsonData.items()):
        # print("key:", value[0], "value:", value[1])
        fileName = dstPath + "\\" + value[0] + ".json"
        #print("fileName:", fileName)
        strJson = json.dumps(value[1])
        with open(fileName, "w", encoding='utf-8') as file:
            #print(strJson)
            file.write(strJson)



def parseExcel(fileName, c):
    #fileName = "D:\\work\\dexuan\\2501\\play_2501.xlsx"
    colName = 0
    colEvent = 1
    colStyle = 3
    colScope = 4
    colGame = 5


    sheet1 = "第一批视频"
    sheet2 = "第二批视频"

    df = pd.read_excel(fileName, sheet_name=sheet1)
    row_count = df.shape[0]
    print(f'行数: {row_count}')
    # row_count = 2
    for row in range(1, row_count):
        #print("---------------------------------------------------------")
        strName  = df.iloc[row, colName]  # 读取第row行，第column列的数据
        strEvent = df.iloc[row, colEvent]  # 读取第row行，第column列的数据
        strStyle = df.iloc[row, colStyle]  # 读取第row行，第column列的数据
        strScope = df.iloc[row, colScope]  # 读取第row行，第column列的数据
        strGame  = df.iloc[row, colGame]  # 读取第row行，第column列的数据

        AppendStyle(c, strStyle, strGame, strEvent, strScope, strName, False)
        # AppendStyle(c, strStyle, strGame, strEvent, strScope, strName, False)


    df2 = pd.read_excel(fileName, sheet_name=sheet2)
    row_count = df2.shape[0]
    print(f'第二批视频行数: {row_count}')

    row_count = df2.shape[0]
    print(f'行数: {row_count}')
    for row in range(1, row_count):
        strName  = df2.iloc[row, colName]  # 读取第row行，第column列的数据
        strEvent = df2.iloc[row, colEvent]  # 读取第row行，第column列的数据
        strStyle = df2.iloc[row, colStyle]  # 读取第row行，第column列的数据
        strScope = df2.iloc[row, colScope]  # 读取第row行，第column列的数据
        strGame  = df2.iloc[row, colGame]  # 读取第row行，第column列的数据

        AppendStyle(c, strStyle, strGame, strEvent, strScope, strName, True)



if __name__ == '__main__':
    c = {
       # "kill": [1,7]
    }


    AppendStyle(c, "erciyuan", "APEX", "victory",  1, "erciyuan_01_begin_victory", True)
    AppendStyle(c, "erciyuan", "APEX", "victory", 0, "erciyuan_01_begin_victory", False)
    AppendStyle(c, "guichu", "APEX", "victory", 1, "erciyuan_01_begin_victory", True)



    excelFile = "d:\\tmp\\素材拆分1129.xlsx"
    # parseExcel(excelFile, c)
    #
    dstPath = "d:\\tmp\\styleFile"
    SaveLocalData(dstPath, c)

    print(c)
    print("finish ...")
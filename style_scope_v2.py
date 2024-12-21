import os
import shutil
import json
import pandas as pd

from utility import *
from hl_public import *


sheet1 = "第一批视频"
sheet2 = "第二批视频"
colName = 0
colEvent = 1
colEffect = 2
colStyle = 3
colScope = 4
# colGame = 5
colGame_LOL = 5
colGame_DOTA2 = 6
colGame_PUBG = 7
colGame_TANKS = 8
colGame_CS2 = 9
colGame_NARAKA = 10
colGame_APEX = 11
colGame_WARSHIPS = 12

def GetStyleIndex(strName, bSecond):
    # print("---------strName：", strName)
    l = strName.split("_")
    styleName = l[0]
    strIndex = l[1]
    try:
        styleIndex = int(strIndex)
    except ValueError:
        return 0
    if((bSecond == True) and (styleName != "fugu") and (styleName != "jike")):
        styleIndex += 25

    return styleIndex

def CheckGameType(col, strName):
    if(is_nan(strName)):
        return 0
    strName = strName.strip()
    if (col == colGame_LOL and strName == "LOL"):
        return 1
    elif (col == colGame_DOTA2 and strName == "DOTA2"):
        return 2
    elif (col == colGame_PUBG and strName == "PUBG"):
        return 4
    elif (col == colGame_TANKS and strName == "WORLD_OF_TANKS"):
        return 5
    elif (col == colGame_CS2 and strName == "CS2"):
        return 6
    elif (col == colGame_NARAKA and strName == "NARAKA"):
        return 7
    elif (col == colGame_APEX and strName == "APEX"):
        return 8
    elif (col == colGame_WARSHIPS and strName == "WORLD_OF_WARSHIPS"):
        return 10
    else:
        print("check game type failed, strName:", strName, " col:", col)
        return 0
    pass

def update_dict(dict, key, value):
    if (values := dict.get(key)) is None:
        dict[key] = values = []
    if value not in values:
        values.append(value)

def CheckEffect(str):
    if str is None:
        return 0

    strEffect = str.strip()
    if strEffect == "effect":
        return 1
    elif strEffect == "word":
        return 2
    else:
        return 0

def ParseGameDetails(c, df, bSecond):
    row_count = df.shape[0]
    print(f'game 行数: {row_count}')
    for row in range(1, row_count):
        strName  = df.iloc[row, colName].strip()  # 读取第row行，第column列的数据
        styleIndex = GetStyleIndex(strName, bSecond)
        strStyleType = df.iloc[row, colStyle].strip()  # 读取第row行，第column列的数据
        styleIndex = 100 * GetStyleType(strStyleType) + styleIndex
        for game_col in range(colGame_LOL, colGame_WARSHIPS+1):
            strGame = df.iloc[row, game_col]
            gameType = CheckGameType(game_col, strGame)
            if(gameType>0):
                update_dict(c, gameType, styleIndex)

# 解析gamelie
def ParseGame(fileName, dstPath):
    c = {}
    df = pd.read_excel(fileName, sheet_name=sheet1)
    ParseGameDetails(c, df, False)
    df2 = pd.read_excel(fileName, sheet_name=sheet2)
    ParseGameDetails(c, df2, True)

    SaveDictFile(dstPath + "\\games.json", c)
    return c

def ParseEventDetails(c, df, bSecond):
    row_count = df.shape[0]
    print(f'event 行数: {row_count}')
    for row in range(1, row_count):
        # print("---------------------------------------------------------")
        strName = df.iloc[row, colName].strip()
        styleIndex = GetStyleIndex(strName, bSecond)
        strStyleType = df.iloc[row, colStyle].strip()
        styleIndex = 100 * GetStyleType(strStyleType) + styleIndex
        strEvent = df.iloc[row, colEvent].strip()
        gEvent = GetGameEvent(strEvent)
        update_dict(c, gEvent, styleIndex)
def ParseEvent(fileName, dstPath):
    c = {}
    df = pd.read_excel(fileName, sheet_name=sheet1)
    ParseEventDetails(c, df, False)

    df2 = pd.read_excel(fileName, sheet_name=sheet2)
    ParseEventDetails(c, df2, True)

    SaveDictFile(dstPath + "\\events.json", c)
    return c

def ParseScopeDetail(c, df, bSecond):
    row_count = df.shape[0]
    print(f'scope 行数: {row_count}')
    # row_count = 3
    for row in range(1, row_count):
        # print("---------------------------------------------------------")
        strName = df.iloc[row, colName].strip()  # 读取第row行，第column列的数据
        styleIndex = GetStyleIndex(strName, bSecond)
        scope = df.iloc[row, colScope]
        if (scope < 1):
            continue
        strEffect = df.iloc[row, colEffect].strip()  # 读取第row行，第column列的数据
        effectFlag = CheckEffect(strEffect)
        if effectFlag == 0:
            continue
        styleIndex += 100 * effectFlag

        strStyleType = df.iloc[row, colStyle].strip()  # 读取第row行，第column列的数据
        styleType = GetStyleType(strStyleType)
        styleIndex += 1000 * styleType

        strEvent = df.iloc[row, colEvent].strip()
        eventType = GetGameEvent(strEvent)
        styleIndex += 10000 * eventType

        for game_col in range(colGame_LOL, colGame_WARSHIPS + 1):
            strGame = df.iloc[row, game_col]  # 读取第row行，第column列的数据
            gameType = CheckGameType(game_col, strGame)
            if (gameType > 0):
                tmpIdx = styleIndex + 100000 * gameType
                update_dict(c, gameType, tmpIdx)

def parseScope(fileName, dstPath):
    c = {}
    df = pd.read_excel(fileName, sheet_name=sheet1)
    ParseScopeDetail(c, df, False)

    df2 = pd.read_excel(fileName, sheet_name=sheet2)
    ParseScopeDetail(c, df2, True)

    SaveDictFile(dstPath+"\\effect_scope.json", c)

    return c

def GetStylelist(srcList, type):
    ret = []
    for key, value in enumerate(srcList):
        if ((int)(value / 100) == type):
            idx = value % 100
            ret.append(idx)
    return ret


def GetScopeEffectStyleIdx(gameType, styleType, eventType):
    ret = []
    srcList = cScope[gameType]
    for key, value in enumerate(srcList):
        sType = (int)(value / 1000) % 10
        eType = (int)(value / 10000) % 10
        # gType = (int)(value / 100000) % 100

        if(sType == styleType and eType == eventType):
            styleIdx = int(value % 1000)
            styleIdx = styleIdx % 100
            ret.append(styleIdx)

    return ret

def GetEffectStyleIndex(gameType, styleType, eventType, bSelected):
    if bSelected:
        ret = GetScopeEffectStyleIdx(gameType, styleType, eventType)
        return ret
        #ret = MergeList(ret, selList)
    else:
        ret = MergeList(cGame[gameType], cEvent[eventType])
        ret = GetStylelist(ret, styleType)
        return ret

def MergeList(l1, l2):
    return list(set(l1) & set(l2))

if __name__ == '__main__':
    dstPath = "d:\\tmp\\styleFile"
    excelFile = "d:\\tmp\\素材拆分1220.xlsx"

    global cGame
    global cEvent
    global cScope

    cGame = ParseGame(excelFile, dstPath)
    cEvent = ParseEvent(excelFile, dstPath)
    cScope = parseScope(excelFile, dstPath)

    gameTypeList = [1, 2, 4, 5, 6, 7, 8, 10]  # 穿越火线不支持
    styleTypeList = [2, 3, 4, 5, 6, 7, 8]  # 素材风格
    eventTypeList = [0, 2, 3, 4, 5]  # 不包含 1 死亡

    # print(cGame[9])
    a1 = {}
    a2 = {}
    for keyGame, valueGame in enumerate(gameTypeList):
        for keyStyle, valueStyle in enumerate(styleTypeList):
            for keyEvent, valueEvent in enumerate(eventTypeList):
                strKey = "{0}-{1}-{2}".format(valueGame, valueStyle, valueEvent)
                value_all = GetEffectStyleIndex(valueGame, valueStyle, valueEvent, False)
                value_selected = GetEffectStyleIndex(valueGame, valueStyle, valueEvent, True)
                a1[strKey] = value_all
                a2[strKey] = value_selected

    SaveDictFile("d:\\tmp\\all.json", a1)
    SaveDictFile("d:\\tmp\\selected.json", a2)
    print("finish")

    # gameTypeList = [5]  # 穿越火线不支持
    # styleTypeList = [2, 3, 4, 5, 6, 7, 8]   # 素材风格
    # eventTypeList = [0, 2, 3, 4, 5]   # 不包含 1 死亡


    # GetEffectStyleIndex(5, 6, 0, True)

    # GetScopeEffectStyleIdx(4, 5, 3)


    # idx = 0
    # value = 602
    # if ((int)(value / 100) == 6):
    #     idx = value % 100
    # print(idx)
    #
    # print(value/100)

    # # 1 普通模式
    # for gameKey, gameValue in enumerate(gameTypeList):
    #     # print(cGame[gameValue])
    #     for styleKey, styleValue in enumerate(cGame[gameValue]):
    #
    #         print("----------------")
    #         print(styleValue)

        # print("i:", i , " val:", val)


    # 2 精选模式


    # # test case
    # match = [0, 0, 2, 5]
    # match2 = [3, 5, 2,]
    # mmm = MergeList(match, match2)
    # print("mm:", mmm)
    # select = False
    # gameType = 4
    # styleType = 6
    #
    # m1 = MergeList(cGame[gameType], cEvent[2])
    # if(select):
    #     m1 = cScope[1]
    # print("m1:", m1)


    # df = pd.read_excel(excelFile, sheet_name=sheet1)
    # row_count = df.shape[0]
    # #strName = df.iloc[11, colGame_DOTA2].strip()  # 读取第row行，第column列的数据
    # strName = df.iloc[11, colGame_TANKS]
    # if(is_nan(strName)):
    #     print( "not ")
    # else:
    #     print(("ssss"))
    # print(strName)

    pass
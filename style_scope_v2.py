import os
import shutil
import json
import pandas as pd

from utility import *
from hl_public import *
from datetime import datetime


sheet1 = "第一批视频"
sheet2 = "第二批视频"
sheet3 = "第三批视频"
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
colGame_RAINBOW6 = 13
colGame_VAROLANT = 14
colGame_FORTNITE = 15
colGame_DESTINY2 = 16
colGame_OW2 = 17
colGame_BATTLEFIELD2042 = 18
colGame_WUKONG = 19
colGame_SF6 = 20
colGame_ALL = 21


# 自定义枚举值
selectedMode = 2    # 精选模式
all_games = 100     # 适合所有游戏
all_events = 100    # 所有事件

tranName = "transition"

gameTypeList = [1, 2, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17]  # 穿越火线不支持
styleTypeList = [2, 3, 4, 5, 6, 7, 8]  # 素材风格
eventTypeList = [0, 2, 3, 4, 5, 11, 12]  # 不包含 1 死亡

def InvalidRow(rowName):
    pos = rowName.find("wukong_nodamage")
    return pos != -1

def GetTranIndex(strName):
    l = strName.split("_")
    strIndex = l[1]
    tranFlag = l[2]
    if(tranFlag != tranName):
        return 0
    try:
        tranIndex = int(strIndex)
    except ValueError:
        return 0
    return tranIndex

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

    # UNKNOWN = 0,
    # LOL,
    # DOTA2,
    # CROSSFIRE, // 穿越火线
    # PUBG, // 吃鸡
    # WORLD_OF_TANKS, // 坦克世界
    # CS2,
    # NARAKA, // 永劫无间
    # APEX,
    # FORTNITE, // 堡垒之夜
    # WORLD_OF_WARSHIPS, // 战舰世界
    # OVER_WATCH, // 守望先锋
    # VALORANT, // 无畏契约
    # DESTINY2, // 命运2
    # BF2042, // 战地风云2042
    # RAINBOW6, // 彩虹六号: 围攻
    # WUKONG, // 黑悟空
    # Street_Fighter6, // 街霸6

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
    elif (col == colGame_RAINBOW6 and strName == "RAINBOW6"):
        return 15 # 彩虹六号
    elif (col == colGame_VAROLANT and strName == "VAROLANT"):
        return 12 # 无畏契约
    elif (col == colGame_FORTNITE and strName == "FORTNITE"):
        return 9 # 堡垒之夜
    elif (col == colGame_DESTINY2 and strName == "DESTINY2"):
        return 13 #命运2
    elif (col == colGame_OW2 and strName == "OW2"):
        return 11 #守望先锋
    elif (col == colGame_BATTLEFIELD2042 and strName == "BATTLEFIELD2042"):
        return 14 #战地风云2042
    elif (col == colGame_WUKONG and strName == "WUKONG"):
        return 16 #黑悟空
    elif (col == colGame_SF6 and strName == "SF6"):
        return 17 #街霸
    elif (col == colGame_ALL and strName == "ALL"):
        return all_games  # 全部
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
    if strEffect == "effect" or strEffect == "effect01":
        return 1
    elif strEffect == "word" or strEffect == "effect02":
        return 2
    elif strEffect == "begin" or strEffect == "end" or strEffect == "transition":
        return 0
    else:
        print(f"check effect failed: {strEffect}")
        return 0

def ParseGameDetails(c, df, bSecond):
    row_count = df.shape[0]
    columns_cnt = df.shape[1]
    print(f'game 行数: {row_count}')
    print(f"game 列数: {columns_cnt}")
    for row in range(1, row_count):
        strName  = df.iloc[row, colName].strip()  # 读取第row行，第column列的数据
        if(InvalidRow(strName) == True):
            print("sssssssssss")
            continue
        styleIndex = GetStyleIndex(strName, bSecond)
        strStyleType = df.iloc[row, colStyle].strip()  # 读取第row行，第column列的数据
        styleType = GetStyleType(strStyleType)
        if(styleType == None):
            print(f"ParseGameDetails styleType is none, {strStyleType}")
            continue
        styleIndex = 100 * styleType + styleIndex
        for game_col in range(colGame_LOL, columns_cnt):
            strGame = df.iloc[row, game_col]
            gameType = CheckGameType(game_col, strGame)
            if (gameType == 0):
                continue
            elif (gameType == all_games):
                for gameIdx in range(1, 17):
                    if gameIdx == 3:
                        # 过滤掉穿越火线
                        continue
                    update_dict(c, gameIdx, styleIndex)
            else:
                update_dict(c, gameType, styleIndex)

# 解析gamelie
def ParseGame(fileName, dstPath):
    c = {}
    df = pd.read_excel(fileName, sheet_name=sheet1)
    ParseGameDetails(c, df, False)
    df2 = pd.read_excel(fileName, sheet_name=sheet2)
    ParseGameDetails(c, df2, True)
    df3 = pd.read_excel(fileName, sheet_name=sheet3)
    ParseGameDetails(c, df3, False)

    # SaveDictFile(dstPath + "\\games.json", c)
    return c

def ParseEventDetails(c, df, bSecond):
    row_count = df.shape[0]
    print(f'event 行数: {row_count}')
    for row in range(1, row_count):
        # print("---------------------------------------------------------")
        strName = df.iloc[row, colName].strip()
        if(InvalidRow(strName) == True):
            continue
        styleIndex = GetStyleIndex(strName, bSecond)
        strStyleType = df.iloc[row, colStyle].strip()
        styleIndex = 100 * GetStyleType(strStyleType) + styleIndex
        strEvent = df.iloc[row, colEvent].strip()
        eventType = GetGameEvent(strEvent)

        if eventType is None:
            print(f"parese event failed, row:{row}, bSecond:{bSecond}")
            continue
        elif eventType == all_events:
            for eIdx in range(0, 6):
                if eIdx == 1:
                    # 去掉死亡事件
                    continue
                update_dict(c, eIdx, styleIndex)
        else:
            update_dict(c, eventType, styleIndex)

def ParseEvent(fileName, dstPath):
    c = {}
    df = pd.read_excel(fileName, sheet_name=sheet1)
    ParseEventDetails(c, df, False)

    df2 = pd.read_excel(fileName, sheet_name=sheet2)
    ParseEventDetails(c, df2, True)

    df3 = pd.read_excel(fileName, sheet_name=sheet3)
    ParseEventDetails(c, df3, False)

    # SaveDictFile(dstPath + "\\events.json", c)
    return c

def ParseScopeDetail(c, df, bSecond):
    row_count = df.shape[0]
    columns_cnt = df.shape[1]
    print(f'scope 行数: {row_count}')
    print(f'scope 列数: {columns_cnt}')
    # row_count = 3
    for row in range(1, row_count):
        # print("---------------------------------------------------------")
        styleIndex = 0
        strName = df.iloc[row, colName].strip()  # 读取第row行，第column列的数据
        if(InvalidRow(strName) == True):
            continue
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
        if eventType is None:
            print(f"parse scope failed, row:{row}, bSecond:{bSecond}")

        for game_col in range(colGame_LOL, columns_cnt):
            strGame = df.iloc[row, game_col]  # 读取第row行，第column列的数据
            gameType = CheckGameType(game_col, strGame)

            if (gameType <= 0):
                continue
            elif (gameType == all_games):
                for gameIdx in gameTypeList:
                    num = styleIndex + 10000 * gameIdx
                    if (eventType == all_events):
                        for oneEventType in eventTypeList:
                            update_dict(c, oneEventType, num)
                    else:
                        update_dict(c, eventType, num)
            if (gameType > 0):
                num = styleIndex + 10000 * gameType
                if (eventType == all_events):
                    for oneEventType in eventTypeList:
                        update_dict(c, oneEventType, num)
                else:
                    update_dict(c, eventType, num)
                #update_dict(c, eventType, num)


def parseScope(fileName, dstPath):
    c = {}
    df = pd.read_excel(fileName, sheet_name=sheet1)
    ParseScopeDetail(c, df, False)

    df2 = pd.read_excel(fileName, sheet_name=sheet2)
    ParseScopeDetail(c, df2, True)

    df3 = pd.read_excel(fileName, sheet_name=sheet3)
    ParseScopeDetail(c, df3, False)

    # SaveDictFile(dstPath+"\\effect_scope.json", c)

    return c

def ParseTranDetail(c, df):
    row_count = df.shape[0]
    columns_cnt = df.shape[1]
    print(f'tran 行数: {row_count}')
    print(f'Tran 列数: {columns_cnt}')
    for row in range(1, row_count):
        # print("---------------------------------------------------------")
        strName = df.iloc[row, colName].strip()  # 读取第row行，第column列的数据
        if(InvalidRow(strName) == True):
            continue
        TranIndex = GetTranIndex(strName)
        if(TranIndex == 0):
            continue

        strStyleType = df.iloc[row, colStyle].strip()  # 读取第row行，第column列的数据
        styleType = GetStyleType(strStyleType)
        scopeType = int(df.iloc[row, colScope])
        # print(f"       style:{styleType}, tranIdx:{TranIndex}")
        TranIndex += 100 * styleType
        TranIndex += 1000 * scopeType
        # print(f"finish style:{styleType}, tranIdx:{TranIndex}")
        # TranIndex 的值 为 ： 比如 二次元+第53套 (二次元 为4)

        # 则 TranIndex = 453
        # 加上精选  如果是精选 则 TranIndex = 1453
        #          如果不是精选 则 TranIndex = 453

        for game_col in range(colGame_LOL, columns_cnt):
            strGame = df.iloc[row, game_col]  # 读取第row行，第column列的数据
            gameType = CheckGameType(game_col, strGame)

            if (gameType <= 0):
                continue
            elif (gameType == all_games):
                for gameIdx in range(1, 17):
                    if gameIdx == 3:
                        # 过滤掉穿越火线
                        continue
                    # print(f"all game, gameidx:{gameIdx}, TranIndex:{TranIndex}")
                    update_dict(c, gameIdx, TranIndex)
            else:
                # print(f"one game, gameidx:{gameType}, TranIndex:{TranIndex}")
                update_dict(c, gameType, TranIndex)

def ParseTran(fileName, dstPath):
    c = {}

    # 转场只针对 第三批视频
    df3 = pd.read_excel(fileName, sheet_name=sheet3)
    ParseTranDetail(c, df3)
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
    srcList = cScope[eventType]
    for key, value in enumerate(srcList):
        sType = (int)(value / 1000) % 10
        gType = (int)(value / 10000) % 100
        # gType = (int)(value / 100000) % 100

        if(sType == styleType and gType == gameType):
            styleIdx = int(value % 1000)
            styleIdx = styleIdx % 100
            if styleIdx not in ret:
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

# 万能素材
def AppendGoodStyle(dictGame, dictEvent, dictScope):
    dictGood = {
        "2": [9],
        "3": [5],
        "4": [1],
        "5": [1],
        "6": [42,3],
        "7": [6],
        "8": [8]
    }

    gameTypeList = [1, 2, 4, 5, 6, 7, 8, 10]  # 穿越火线不支持
    eventTypeList = [0, 2, 3, 4, 5]  # 不包含 1 死亡

    for key, value in dictGood.items():
        for detail in value:
            StyleIndex = int(key) * 100 + detail
            for gType in gameTypeList:
                update_dict(dictGame, gType, StyleIndex)
            for eType in eventTypeList:
                update_dict(dictEvent, eType, StyleIndex)

    for eType in eventTypeList:
        for gType in gameTypeList:
            for key, value in dictGood.items():
                for detail in value:
                    StyleIdxEffct = 100 * 1 + detail + int(key) * 1000 + gType * 10000
                    StyleIdxWord = 100 * 2 + detail + int(key) * 1000 + gType * 10000

                    update_dict(dictScope, eType, StyleIdxEffct)
                    update_dict(dictScope, eType, StyleIdxWord)
    pass

def MergeList(l1, l2):
    return list(set(l1) & set(l2))

if __name__ == '__main__':
    # excelFile = "d:\\tmp\\素材拆分1230.xlsx"
    excelFile = "d:\\tmp\\素材拆分20250404-调整游戏列表.xlsx"

    # dstPath = "d:\\tmp\\styleFile"
    # dstPath = "d:\\tmp\\styleFile0331"
    dstPath = "d:\\tmp\\styleFile0404"

    CheckAndCreatePath(dstPath)

    global cGame
    global cEvent
    global cScope

    cGame = {}
    cEvent = {}
    cScope = {}
    cTran = {}
    cGame = ParseGame(excelFile, dstPath)
    cEvent = ParseEvent(excelFile, dstPath)
    cScope = parseScope(excelFile, dstPath)
    cTran = ParseTran(excelFile, dstPath)

    AppendGoodStyle(cGame, cEvent, cScope)
    #
    # save to disk
    SaveDictFile(dstPath + "\\games.json", cGame)
    SaveDictFile(dstPath + "\\events.json", cEvent)
    SaveDictFile(dstPath + "\\effect_scope.json", cScope)
    SaveDictFile(dstPath + "\\trans.json", cTran)
    #
    # gameTypeList = [1, 2, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17]  # 穿越火线不支持
    # styleTypeList = [2, 3, 4, 5, 6, 7, 8]  # 素材风格
    # eventTypeList = [0, 2, 3, 4, 5]  # 不包含 1 死亡
    #
    # # print(cGame[9])
    # a1 = {}
    # a2 = {}
    # for keyGame, valueGame in enumerate(gameTypeList):
    #     for keyStyle, valueStyle in enumerate(styleTypeList):
    #         for keyEvent, valueEvent in enumerate(eventTypeList):
    #             strKey = "{0}-{1}-{2}".format(valueGame, valueStyle, valueEvent)
    #             value_all = GetEffectStyleIndex(valueGame, valueStyle, valueEvent, False)
    #             value_selected = GetEffectStyleIndex(valueGame, valueStyle, valueEvent, True)
    #             a1[strKey] = value_all
    #             a2[strKey] = value_selected
    #
    # SaveDictFile("d:\\tmp\\all.json", a1)
    # SaveDictFile("d:\\tmp\\selected.json", a2)


    print("finish")

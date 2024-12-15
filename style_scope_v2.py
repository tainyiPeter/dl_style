import os
import shutil
import json
import pandas as pd

sheet1 = "第一批视频"
sheet2 = "第二批视频"
colName = 0
colEvent = 1
colEffect = 2
colStyle = 3
colScope = 4
colGame = 5


def GetStyleIndex(strName, bSecond):
    # print("---------strName：", strName)
    l = strName.split("_")
    styleName = l[0]
    strIndex = l[1]
    styleIndex = int(strIndex)
    if((bSecond == True) and (styleName != "fugu") and (styleName != "jike")):
        styleIndex += 25

    return styleIndex

def GetGameType(strType):
    gameStringToType = {
        "LOL": 1,
        "DOTA2": 2,
        #"CROSSFIRE": 3,
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

def SaveFile(strFileName, c):
    dstPath = os.path.dirname(strFileName)
    if not os.path.exists(dstPath):
        os.makedirs(dstPath)  # 创建路径
    strJson = json.dumps(c)
    with open(strFileName, "w", encoding='utf-8') as file:
        # print(strJson)
        file.write(strJson)
    pass
def GetGameEvent(strEvent):
    gameEventToInt = {
        "kill":0,
        "assist":2,
        "knock down":3,
        "defeat":4,
        "victory":5
    }

    if(strEvent not in gameEventToInt):
        print("get game event failed,", strEvent)
        return -1
    else:
        return gameEventToInt[strEvent]

def GetStyleIdx(strName):
    #strName = strName.split()
    stringToType = {
        "gaoran": 2,
        "guichu":3,
        "erciyuan": 4,
        "chaoxianshi": 5,
        "menghuan":6,
        "fugu":7,
        "jike":8,
    }
    if(strName not in stringToType):
        print("get style type failed,", strName)
        return 0
    else:
        return stringToType[strName]

def upsert_dict(dict_var, key, value):
    if key in dict_var:
        l = dict_var[key]
        l.append(value)
        l = list(set(l))
        dict_var[key] = l
    else:
        dict_var.setdefault(key, [value])

# 解析gamelie
def ParseGame(fileName, dstPath):
    c = {}
    df = pd.read_excel(fileName, sheet_name=sheet1)
    row_count = df.shape[0]
    print(f'行数: {row_count}')
    # row_count = 3
    for row in range(1, row_count):
        #print("---------------------------------------------------------")
        strName  = df.iloc[row, colName].strip()  # 读取第row行，第column列的数据
        styleIndex = GetStyleIndex(strName, False)
        strStyle = df.iloc[row, colStyle].strip()  # 读取第row行，第column列的数据
        strGame = df.iloc[row, colGame].strip()  # 读取第row行，第column列的数据
        gameType = GetGameType(strGame)
        styleIndex = 100 * GetStyleIdx(strStyle) + styleIndex
        upsert_dict(c, gameType, styleIndex)

    df2 = pd.read_excel(fileName, sheet_name=sheet2)
    row_count = df2.shape[0]
    print(f'行数: {row_count}')
    for row in range(1, row_count):
        #print("---------------------------------------------------------")
        strName = df2.iloc[row, colName].strip()  # 读取第row行，第column列的数据
        styleIndex = GetStyleIndex(strName, True)
        strStyle = df2.iloc[row, colStyle].strip()  # 读取第row行，第column列的数据
        strGame = df2.iloc[row, colGame].strip()  # 读取第row行，第column列的数据
        gameType = GetGameType(strGame)
        styleIndex = 100 * GetStyleIdx(strStyle) + styleIndex
        upsert_dict(c, gameType, styleIndex)

    all = c.pop(100)
    for key, value in enumerate(c.items()):
        c[value[0]] = c[value[0]] + all

    SaveFile(dstPath + "\\games.json", c)
    return c
    pass

def ParseEvent(fileName, dstPath):
    c = {}

    df = pd.read_excel(fileName, sheet_name=sheet1)
    row_count = df.shape[0]
    print(f'行数: {row_count}')
    # row_count = 3
    for row in range(1, row_count):
        # print("---------------------------------------------------------")
        strName = df.iloc[row, colName].strip()  # 读取第row行，第column列的数据
        styleIndex = GetStyleIndex(strName, False)
        strStyle = df.iloc[row, colStyle].strip()  # 读取第row行，第column列的数据

        styleIndex = 100 * GetStyleIdx(strStyle) + styleIndex
        strEvent = df.iloc[row, colEvent].strip()  # 读取第row行，第column列的数据
        gEvent = GetGameEvent(strEvent)
        upsert_dict(c, gEvent, styleIndex)

    df2 = pd.read_excel(fileName, sheet_name=sheet2)
    row_count = df2.shape[0]
    print(f'行数: {row_count}')
    # row_count = 3
    for row in range(1, row_count):
        # print("---------------------------------------------------------")
        strName = df2.iloc[row, colName].strip()  # 读取第row行，第column列的数据
        styleIndex = GetStyleIndex(strName, True)
        strStyle = df2.iloc[row, colStyle].strip()  # 读取第row行，第column列的数据

        styleIndex = 100 * GetStyleIdx(strStyle) + styleIndex
        strEvent = df2.iloc[row, colEvent].strip()  # 读取第row行，第column列的数据
        gEvent = GetGameEvent(strEvent)
        upsert_dict(c, gEvent, styleIndex)

    SaveFile(dstPath + "\\events.json", c)
    return c
    pass

def parseScope(fileName, dstPath):
    c = {}
    df = pd.read_excel(fileName, sheet_name=sheet1)
    row_count = df.shape[0]
    print(f'行数: {row_count}')
    # row_count = 3
    for row in range(1, row_count):
        # print("---------------------------------------------------------")
        strName = df.iloc[row, colName].strip()  # 读取第row行，第column列的数据
        styleIndex = GetStyleIndex(strName, False)
        scope = df.iloc[row, colScope]
        if(scope < 1):
            continue
        strEffect = df.iloc[row, colEffect].strip()  # 读取第row行，第column列的数据
        effectFlag = 0
        if strEffect == "effect":
            effectFlag = 1
        elif strEffect == "word":
            effectFlag = 2
        if effectFlag == 0:
            continue
        styleIndex += 100 * effectFlag

        strStyle = df.iloc[row, colStyle].strip()  # 读取第row行，第column列的数据
        styleType = GetStyleIdx(strStyle)
        styleIndex += 1000 * styleType

        strEvent = df.iloc[row, colEvent].strip()
        eventType = GetGameEvent(strEvent)
        styleIndex += 10000 * eventType

        strGame = df.iloc[row, colGame].strip()
        gameType = GetGameType(strGame)
        styleIndex += 100000 * gameType

        upsert_dict(c, 2, styleIndex)

    df2 = pd.read_excel(fileName, sheet_name=sheet2)
    row_count = df2.shape[0]
    print(f'行数: {row_count}')
    # only test
    # row_count = 5
    for row in range(1, row_count):
        # print("---------------------------------------------------------")
        strName = df2.iloc[row, colName].strip()  # 读取第row行，第column列的数据
        styleIndex = GetStyleIndex(strName, True)

        scope = df2.iloc[row, colScope]
        if (scope < 1):
            continue
        strEffect = df2.iloc[row, colEffect].strip()  # 读取第row行，第column列的数据
        effectFlag = 0
        if strEffect == "effect":
            effectFlag = 1
        elif strEffect == "word":
            effectFlag = 2
        if effectFlag == 0:
            continue
        styleIndex += 100 * effectFlag

        strStyle = df2.iloc[row, colStyle].strip()  # 读取第row行，第column列的数据
        styleType = GetStyleIdx(strStyle)
        styleIndex += 1000 * styleType

        strEvent = df2.iloc[row, colEvent].strip()
        eventType = GetGameEvent(strEvent)
        styleIndex += 10000 * eventType

        strGame = df2.iloc[row, colGame].strip()
        gameType = GetGameType(strGame)
        styleIndex += 100000 * gameType

        upsert_dict(c, 2, styleIndex)

    SaveFile(dstPath+"\\effect_scope.json", c)

    return c
    pass

def MergeList(l1, l2):
    return list(set(l1) & set(l2))

    pass
if __name__ == '__main__':
    dstPath = "d:\\tmp\\styleFile"
    excelFile = "d:\\tmp\\素材拆分1129.xlsx"

    cGame = ParseGame(excelFile, dstPath)
    cEvent = ParseEvent(excelFile, dstPath)
    cScope = parseScope(excelFile, dstPath)


    # test case
    match = [0, 0, 2, 5]
    match2 = [3,5, 2,]
    mmm = MergeList(match, match2)
    print("mm:", mmm)
    select = False
    gameType = 4
    styleType = 6

    m1 = MergeList(cGame[gameType], cEvent[2])
    if(select):
        m1 = cScope[1]
    print("m1:", m1)

    # print(cGame[4])

    # for i in enumerate(match):
    #     print (cGame["APEX"])
    #     break
    #     # print(i, ' ', i[1])


    pass
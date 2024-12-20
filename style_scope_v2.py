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
# colGame = 5
colGame_LOL = 5
colGame_DOTA2 = 6
colGame_PUBG = 7
colGame_TANKS = 8
colGame_CS2 = 9
colGame_NARAKA = 10
colGame_APEX = 11
colGame_WARSHIPS = 12


def is_nan(s):
    try:
        f = float(s)
        return f != f
    except ValueError:
        return  False

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
        styleIndex = 100 * GetStyleIdx(strStyle) + styleIndex
        for game_col in range(colGame_LOL, colGame_WARSHIPS+1):
            strGame = df.iloc[row, game_col]
            gameType = CheckGameType(game_col, strGame)
            if(gameType>0):
                upsert_dict(c, gameType, styleIndex)

    df2 = pd.read_excel(fileName, sheet_name=sheet2)
    row_count = df2.shape[0]
    print(f'行数: {row_count}')
    for row in range(1, row_count):
        #print("---------------------------------------------------------")
        strName = df2.iloc[row, colName].strip()  # 读取第row行，第column列的数据
        styleIndex = GetStyleIndex(strName, True)
        strStyle = df2.iloc[row, colStyle].strip()  # 读取第row行，第column列的数据
        styleIndex = 100 * GetStyleIdx(strStyle) + styleIndex
        for game_col in range(colGame_LOL, colGame_WARSHIPS+1):
            # print("[test] game_col:", game_col, " row:", row, " name:", strName)
            strGame = df2.iloc[row, game_col]
            gameType = CheckGameType(game_col, strGame)
            if(gameType>0):
                upsert_dict(c, gameType, styleIndex)
        #upsert_dict(c, gameType, styleIndex)

    # all = c.pop(100)
    # for key, value in enumerate(c.items()):
    #     c[value[0]] = c[value[0]] + all

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
    tmpcnt = 0
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

        for game_col in range(colGame_LOL, colGame_WARSHIPS+1):
            strGame = df.iloc[row, game_col]  # 读取第row行，第column列的数据
            gameType = CheckGameType(game_col, strGame)
            if(gameType>0):
                tmpIdx = styleIndex + 100000 * gameType
                upsert_dict(c, gameType, tmpIdx)

                tmpcnt +=1
                print("scope:cnt", tmpcnt, " gameType:", gameType)

        # strGame = df.iloc[row, colGame].strip()
        # gameType = GetGameType(strGame)
        # styleIndex += 100000 * gameType

        #upsert_dict(c, 2, styleIndex)

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

        for game_col in range(colGame_LOL, colGame_WARSHIPS+1):
            strGame = df2.iloc[row, game_col]  # 读取第row行，第column列的数据
            gameType = CheckGameType(game_col, strGame)
            if(gameType>0):
                tmpIdx = styleIndex + 100000 * gameType
                upsert_dict(c, gameType, tmpIdx)

                tmpcnt +=1
                print("scope 2 :cnt", tmpcnt, " gameType:", gameType)


        # strGame = df2.iloc[row, colGame].strip()
        # gameType = GetGameType(strGame)
        # styleIndex += 100000 * gameType
        #
        # upsert_dict(c, 2, styleIndex)

    SaveFile(dstPath+"\\effect_scope.json", c)

    return c
    pass

def GetBeginEndStyleIndex(gameType, styleType, bSelected):

    pass

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

    pass

if __name__ == '__main__':
    dstPath = "d:\\tmp\\styleFile"
    excelFile = "d:\\tmp\\素材拆分1220.xlsx"

    global cGame
    global cEvent
    global cScope


    cGame = ParseGame(excelFile, dstPath)
    cEvent = ParseEvent(excelFile, dstPath)
    cScope = parseScope(excelFile, dstPath)


    gameTypeList = [1,2,4,5,6,7,8, 10]  # 穿越火线不支持
    styleTypeList = [2, 3, 4, 5, 6, 7, 8]   # 素材风格
    eventTypeList = [0, 2, 3, 4, 5]   # 不包含 1 死亡

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
                pass

    SaveFile("d:\\tmp\\all.json", a1)
    SaveFile("d:\\tmp\\selected.json", a2)


    print(str)

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
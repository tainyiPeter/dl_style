

# 获取素材风格类型
def GetStyleType(strName):
    dict = {
        "gaoran": 2,
        "guichu": 3,
        "erciyuan": 4,
        "chaoxianshi": 5,
        "menghuan": 6,
        "fugu": 7,
        "jike": 8,
    }

    return dict.get(strName)

def GetGameEvent(strEvent):
    dict = {
        "kill": 0,
        "dead": 1,
        "assist": 2,
        "knock down": 3,
        "defeat": 4,
        "victory": 5
    }

    return dict.get(strEvent)

def GetGameType(strType):
    dict = {
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

    return dict.get(strType)
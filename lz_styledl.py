# -*- coding: utf-8 -*-
import httplib2
import json
import sys
import uuid
import time
import os
import HttpUtils
import utility
import pandas as pd
from datetime import datetime

from urllib.parse import urlencode


# legion zone 素材下载ceshi8脚本
# 文档地址：
# https://km.xpaas.lenovo.com/pages/viewpage.action?pageId=464204410

style_version = "v1.0.3"

# 单个素材文件上传地址, 测试地址
ZipUrl = "https://cloud-biz.mbgtest.lenovomm.com/cloud-legionzone/file/uploadFile"
# cecel文件上传地址
ExcelUrl = "https://cloud-biz.mbgtest.lenovomm.com/cloud-legionzone/biz/file/se/uploadFile"

grant_type = "client_credentials"
appId = "1593389727517312"
client_secret = "d248f803532a4d009c4bdecfb5bcd5cc"

# http test
def post_test():
    # 创建HTTP对象
    http = httplib2.Http()

    # 准备POST数据
    url = 'http://httpbin.org/post'
    body = json.dumps({'key': 'value'})  # 将数据转换为JSON字符串
    headers = {'Content-Type': 'application/json'}  # 设置内容类型为JSON

    # 发送POST请求
    response, content = http.request(url, 'POST', body=body, headers=headers)

    # 打印响应状态码和内容
    print('Status:', response.status)
    print('Content:', content.decode('utf-8'))

def get_test():
    # 参数定义
    params = {"key1": "value1", "key2": "value2"}

    # 编码参数并构建 URL
    url = "http://httpbin.org/get?" + urlencode(params)

    print('url:', url)
    # 发送请求
    http = httplib2.Http()
    response, content = http.request(url, "GET")

    # 处理响应
    if response.status == 200:
        data = json.loads(content.decode("utf-8"))
        print("请求成功！参数:", data["args"])
    else:
        print("请求失败，状态码:", response.status)

# 授权接口
def dl_auth(grant_type, cid, secret):
    # 请求的URL
    url = 'https://cloud-pay.mbgtest.lenovomm.com/cloud-auth/oauth/token'

    # 请求体数据
    data = {
        "grant_type": grant_type,
        "client_id": cid,
        "client_secret": secret
    }

    # 将字典编码为 application/x-www-form-urlencoded 格式
    body = urlencode(data)

    # 设置请求头
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': str(len(body))
    }

    # 创建 httplib2.Http 对象
    http = httplib2.Http()

    # 发送 POST 请求
    response, content = http.request(
        url,
        method='POST',
        body=body,
        headers=headers
    )

    # 打印响应状态码和内容
    # print("Status Code:", response.status)
    # print("Response Content:", content.decode('utf-8'))

    return response, content

def GetAuthToken():
    response, content = dl_auth(grant_type, appId, client_secret)
    if(response.status != 200):
        print("get token failed")
        return

    data = json.loads(content)
    return data["access_token"]

    print("Status Code:", response.status)
    print("Response Content:", content.decode('utf-8'))

def GetList():
    reqUrl = "https://cloud-pay.mbgtest.lenovomm.com/cloud-legionzone/api/v1/getClassifyList"
    uuid_str = str(uuid.uuid4())
    timeStamp = int(time.time()) * 1000
    paramList = {
        "appId": appId,
        "nonce": uuid_str,
        "sign_type": "RSA2",
        "timestamp": str(timeStamp)
    }

    sign = HttpUtils.CreateLzSign(paramList)
    paramList["sign"] = sign
    reqUrl += "?"
    reqUrl += urlencode(paramList)
    print(f"reqUrl:{reqUrl}")

    #print(paramList)
    # reqUrl = "https://cloud-pay.mbgtest.lenovomm.com/cloud-legionzone/api/v1/getClassifyList?appId=1593389727517312&nonce=aae3769c-d3f2-4c71-81c8-d200d0dc4763&sign_type=RSA2&timestamp=1741070251617&sign=ChlEO7xFT3jog%2BT1l7w%2BcjZwEQmXk%2FP%2BgBd7JCwt8KLORSWjJ1zoLOKOqLAxrf%2FRh1FJvR7rcA6thejdfSnrD9hhz46%2Bn0qBnigvc59iGqgV5nRPqR2LrOIN5i1sKnXA6ZcU0sFJYUmmMExflydUBMAcKnrcw9GtGUEKmPXZJ4g%3D"
    http = httplib2.Http()
    response, content = http.request(reqUrl,"GET")
    print("----------------------------------------------------------------")
    print('Status:', response.status)
    print('Content:', content.decode('utf-8'))



def GetData(classifyId, pageIdx=1, pageSize=10):
    reqUrl = "https://cloud-pay.mbgtest.lenovomm.com/cloud-legionzone/api/v1/getClassifyDatas"
    uuid_str = str(uuid.uuid4())
    timeStamp = int(time.time()) * 1000
    paramList = {
        "appId": appId,
        "nonce": uuid_str,
        "sign_type": "RSA2",
        "timestamp": str(timeStamp),
        "classifyId": str(classifyId),
        "page": str(pageIdx),
        "pageSize": str(pageSize)
    }

    sign = HttpUtils.CreateLzSign(paramList)
    paramList["sign"] = sign
    reqUrl += "?"
    reqUrl += urlencode(paramList)
    print("requrl:", reqUrl)

    # print(paramList)

    http = httplib2.Http()
    response, content = http.request(reqUrl, "GET")
    print("----------------------------------------------------------------")
    print('Status:', response.status)
    print('Content:', content.decode('utf-8'))

    # OutPut.HttpRespOut(info, content, False)
    # jsonData = json.loads(content)
    # print(jsonData)

def upload_file(url, file_name, token_auth, field_name='file', extra_fields=None):
    # 创建Http对象
    http = httplib2.Http()

    # 定义唯一的boundary
    boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'

    # 构建请求体
    body = []

    # 添加普通字段
    if extra_fields:
        for key, value in extra_fields.items():
            body.append(f'--{boundary}\r\n'.encode('utf-8'))
            body.append(
                f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode('utf-8')
            )
            body.append(f'{value}\r\n'.encode('utf-8'))

    # 添加文件字段
    body.append(f'--{boundary}\r\n'.encode('utf-8'))
    body.append(
        f'Content-Disposition: form-data; name="{field_name}"; filename="{file_name}"\r\n'.encode('utf-8')
    )
    body.append('Content-Type: application/octet-stream\r\n\r\n'.encode('utf-8'))

    # 读取文件内容（二进制模式）
    with open(file_name, 'rb') as f:
        body.append(f.read())
    body.append(f'\r\n--{boundary}--\r\n'.encode('utf-8'))

    # 合并所有部分
    body = b''.join(body)

    # 设置请求头
    headers = {
        'Content-Type': f'multipart/form-data; boundary={boundary}',
        'Content-Length': str(len(body)),
        'Authorization': f'bearer {token_auth}'
    }

    # 发送POST请求
    response, content = http.request(
        uri=url,
        method='POST',
        headers=headers,
        body=body
    )

    return response, content

# def AppendItem(dict, tid, cateId, sha256, style_url, version_num, version_time):
#     if (values := dict.get(tid)) is None:
#         dict[tid] = {}
#
#     values = {
#         "cateId": cateId,
#         "num": tid,
#         "sha256": sha256,
#         "url": style_url,
#         "versionNum": version_num,
#         "versionTime": version_time,
#     }
#     dict[tid] = values

def AppendDefault():
    dict = {}
    dict["categoryId"] = []
    dict["thirdId"] = []
    dict["eleDesc"] = []
    dict["gameDownloadUrl"] = []
    dict["versionNum"] = []
    dict["versionTime"] = []

    return dict
def AppendNum(dict, key, cateId, sha256, style_url, version_num, version_time):
    dict["categoryId"].append(cateId)
    dict["thirdId"].append(key)
    dict["eleDesc"].append(sha256)
    dict["gameDownloadUrl"].append(style_url)
    dict["versionNum"].append(version_num)
    dict["versionTime"].append(version_time)

def SaveDataToExcel(fileName, pageName, data):
    df = pd.DataFrame(data)
    with pd.ExcelWriter(fileName) as writer:
        df.to_excel(writer, sheet_name=pageName, index=False)

def SaveMulsheetToExcel(fileName, mulData):
    print(f"fileName:{fileName}")
    with pd.ExcelWriter(fileName) as writer:
        for key, data in mulData.items():
            df = pd.DataFrame(data)
            df.to_excel(writer, sheet_name=key, index=False)

## type 为 1时 excel
def upTest(type , file_name, token_auth, field_name='file', extra_fields=None):
    url = ZipUrl
    if type == 1:
        url = ExcelUrl
    # 创建Http对象
    http = httplib2.Http()

    # 定义唯一的boundary
    boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'

    # 构建请求体
    body = []

    # 添加普通字段
    if extra_fields:
        for key, value in extra_fields.items():
            body.append(f'--{boundary}\r\n'.encode('utf-8'))
            body.append(
                f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode('utf-8')
            )
            body.append(f'{value}\r\n'.encode('utf-8'))

    # 添加文件字段
    body.append(f'--{boundary}\r\n'.encode('utf-8'))
    body.append(
        f'Content-Disposition: form-data; name="{field_name}"; filename="{file_name}"\r\n'.encode('utf-8')
    )
    body.append('Content-Type: application/octet-stream\r\n\r\n'.encode('utf-8'))

    # 读取文件内容（二进制模式）
    with open(file_name, 'rb') as f:
        body.append(f.read())
    body.append(f'\r\n--{boundary}--\r\n'.encode('utf-8'))

    # 合并所有部分
    body = b''.join(body)

    # 设置请求头
    headers = {
        'Content-Type': f'multipart/form-data; boundary={boundary}',
        'Content-Length': str(len(body)),
        'Authorization': f'bearer {token_auth}'
    }

    # 发送POST请求
    response, content = http.request(
        uri=url,
        method='POST',
        headers=headers,
        body=body
    )

    data = json.loads(content)
    if type == 1:
        return data["message"]
    else:
        return data["data"]

# (300=语音;301=自动；302=高燃；303=鬼畜；304=二次元；305=超现实；306=梦幻;307=复古，308=极客)
def GetCategoryId(stype_name):
    if stype_name == "gaoran":
        return 302
    elif stype_name == "guichu":
        return 303
    elif stype_name == "erciyuan":
        return 304
    elif stype_name == "chaoxianshi":
        return 305
    elif stype_name == "menghuan":
        return 306
    elif stype_name == "fugu":
        return 307
    elif stype_name == "jike":
        return 308
    else:
        return 0
def BatchUpdateZip(token, filePath):
    stype_name = os.path.basename(filePath)
    cateId = GetCategoryId(stype_name)
    if(cateId == 0):
        print(f"get categoryid failed, stype_name:{stype_name}, filePath:{filePath}")
        return {}
    versionNum = style_version
    timeStamp = int(time.time())
    dict = AppendDefault()
    zipFiles = utility.GetFiles(filePath)
    for key, fullName in enumerate(zipFiles):
        sha256 = utility.calculate_file_sha256(fullName)
        fileName = os.path.basename(fullName)
        num = os.path.splitext(fileName)[0]
        url = upTest(0, fullName, token)
        print(f"key:{num}, value:{fullName}, url:{url}")
        AppendNum(dict, num, str(cateId), sha256,  url, versionNum, str(timeStamp))

    return dict

def updataStyles():
    # src = "D:\\tmp\\src123"
    src = "D:\\work\\liuzf\\test\\dst"
    # src = "D:\\work\\liuzf\\test\\dst_test"
    dst = "D:\\work\\liuzf\\test\\dst_test"
    if not os.path.exists(dst):
        os.makedirs(dst)  # 创建路径
    current_time = datetime.now().strftime("lz_uf_%Y-%m-%d_%H-%M-%S")
    dstFile = f"{dst}\\{current_time}.xlsx"
    print(f"dstFile:{dstFile}")

    token = GetAuthToken()
    print(f"token:{token}")
    if (len(token) == 0):
        print("get token failed")
        sys.exit(0)

    mulData = {}
    dirs = utility.GetDirs(src)
    for key, value in enumerate(dirs):
        fileName = value["name"]
        fullName = value["fullname"]
        dict = BatchUpdateZip(token, fullName)
        mulData[fileName] = dict

        # dstName = f"{dst}\\{fileName}.xlsx"
        # SaveDataToExcel(dstName, fileName, dict)
        # print(f"append data {fileName}")
        # suc = upTest(1, dstName, token)
        # print(f"update excel suc:{suc}")

    SaveMulsheetToExcel(dstFile, mulData)
    print(f"save excel to {dstFile}")
    suc = upTest(1, dstFile, token)
    print(f"update excel suc:{suc}")

def SingFileUpdate(fullName):
    token = GetAuthToken()

    url = upTest(0, fullName, token)
    print(f"update url:{url}")



if __name__ == '__main__':
    # updataStyles()
    # GetList()
    # GetData(304)

    #updataStyles()

    # key:47, value:D:\work\liuzf\test\dst\guichu\47.zip, url:None
    SingFileUpdate("D:\\work\\liuzf\\test\\dst\\guichu\\47.zip")

    print(f"finish ...")





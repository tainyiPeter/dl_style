# -*- coding: utf-8 -*-
import httplib2
import hashlib
import json
import HttpUtils
import uuid
import time
import os
import mimetypes

from urllib.parse import urlencode


# legion zone 素材下载ceshi8脚本
# 文档地址：
# https://km.xpaas.lenovo.com/pages/viewpage.action?pageId=464204410

appId = "1593389727517312"

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
    reqUrl = "https://cloud-pay.mbgtest.lenovomm.com/cloud-auth/oauth/token"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    body = {
        "grant_type": grant_type,
        "client_id": cid,
        "client_secret": secret,
    }
    http = httplib2.Http()
    strJsonBody = json.dumps(body)
    response, content = http.request(reqUrl, 'POST', body=strJsonBody, headers=headers)

    # 打印响应状态码和内容
    print('Status:', response.status)
    print('Content:', content.decode('utf-8'))

    # req = http.request.Request(reqUrl,"POST", strJsonBody, head)
    # res = request.urlopen(req)
    # powerData = res.read()
    # jsonData = json.loads(powerData)
    # jsonDataF = json.dumps(jsonData, ensure_ascii=False, indent=1)

    # print(jsonDataF)




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



def GetData(classifyId, pageIdx, pageSize):
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


def upload_file(url, file_path):
    # 获取文件的MIME类型
    content_type, _ = mimetypes.guess_type(file_path)
    if content_type is None:
        content_type = 'application/octet-stream'

    # 创建httplib2的Http对象
    h = httplib2.Http()

    headers = {
        "Content-Type": "multipart/form-data",
        "Authorization": "bearer 6de397e0-187e-4877-83b1-cdbab75dbe62"
    }

    # 读取文件内容
    with open(file_path, 'rb') as f:
        file_content = f.read()

    # 构建multipart表单数据
    body = {
        'file': (os.path.basename(file_path), file_content, content_type)
    }

    # 发送POST请求
    response, content = h.request(url, 'POST', body=body.encode(), headers=headers)

    # 打印响应状态和内容
    print('Response status:', response.status)
    print('Response content:', content)

uploadurl = "https://cloud-biz.mbgtest.lenovomm.com/cloud-legionzone/file/uploadFile"

if __name__ == '__main__':
    filePath = "D:\\tmp\\se.bin"
    upload_file(uploadurl, filePath)
    # dl_auth("client_credentials", "1593389727517312", "d248f803532a4d009c4bdecfb5bcd5cc")
    # GetData(301, 1, 10)
    #GetList()
    #get_test()
    # test()
    print("finish ...")








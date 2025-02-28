import json

import httplib2
import hashlib
import httplib2
import time
import base64

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

sign = "sjdxfnqogbzoun13d971ckh8p"


# 生成密钥对
def gen_public_key():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    return public_key
def Sha256withRSA(message):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    return signature

# legion zone 下载签名
def CreateLzSign(paramData):
    strContent=""
    total = len(paramData);
    paramKey= sorted(paramData.keys())
    idx = 0
    for key in paramKey:
        strContent += key
        strContent += "="
        strContent += paramData[key]
        idx += 1
        if(idx < total):
            strContent += "&"
    print("before base64:", strContent)

    signature = Sha256withRSA(strContent.encode("utf-8"))

    #base64.b64encode(signature).decode("utf-8")
    signature_b64 = base64.b64encode(signature).decode("utf-8")
    print("签名（Base64）:", signature_b64)
    return signature_b64
    #
    # # 原始数据（字符串或字节）
    # data = dataRsa.encode("utf-8")  # 转为字节
    #
    # # Base64 编码
    # encoded_data = base64.b64encode(data)
    # return encoded_data.decode("utf-8")
def CreateSign(paramData, timeStamp):
    strContent=""
    paramKey= sorted(paramData.keys())
    for key in paramKey:
        strContent += paramData[key]
    strContent = sign + strContent + str(timeStamp)
    return hashlib.md5(strContent.encode(encoding='UTF-8')).hexdigest()

def CreatePermitSign(fixed, paramData, timeStamp):
    strContent=""
    paramKey= sorted(paramData.keys())
    for key in paramKey:
        strContent += paramData[key]
    # fixed = "q1NwL2YhXlHBgyt7vvGpRi6MPCOAGxqI"
    # fixed = "Qiw2sBfMw86hugD9OnENgLdp8G8NdKLM"
    strContent = fixed + strContent + str(timeStamp)
    return hashlib.md5(strContent.encode(encoding='UTF-8')).hexdigest()

def CreatePermitPostSign(fixed, content, timeStamp):
    strContent = fixed + content + str(timeStamp)
    return hashlib.md5(strContent.encode(encoding='UTF-8')).hexdigest()


def CreateDYPostSign(paramData):
    appKey_pc="a057406e1b21be4c4eb70b6d0c681da2"
    strContent = ""
    paramKey = sorted(paramData.keys())
    for key in paramKey:
        strContent += key
        strContent += paramData[key]
    strContent = appKey_pc + strContent + appKey_pc
    return hashlib.md5(strContent.encode(encoding='UTF-8')).hexdigest()

def CreateQJBSign(paramData, timeStamp):
    strContent=""
    paramKey= sorted(paramData.keys())
    for key in paramKey:
        strContent += paramData[key]
    strContent = "Qiw2sBfMw86hugD9OnENgLdp8G8NdKLM" + strContent + str(timeStamp)
    return hashlib.md5(strContent.encode(encoding='UTF-8')).hexdigest()

def CreateQLBSign(paramData, timeStamp):
    strContent=""
    paramKey= sorted(paramData.keys())
    for key in paramKey:
        strContent += paramData[key]
    strContent = sign + strContent + str(timeStamp)
    return hashlib.md5(strContent.encode(encoding='UTF-8')).hexdigest()

def CreateQLBNewSign(paramData, timeStamp):
    strContent=""
    paramKey= sorted(paramData.keys())
    for key in paramKey:
        strContent += paramData[key]
    strContent = "f1b511a4912f459b8914f577d2818781" + strContent + str(timeStamp)
    return hashlib.md5(strContent.encode(encoding='UTF-8')).hexdigest()

def CreateQLBSignPost(content, timeStamp):
    strContent = "f1b511a4912f459b8914f577d2818781" + content + str(timeStamp)
    return hashlib.md5(strContent.encode(encoding='UTF-8')).hexdigest()


fdsign = "U7KK2GV5GH68"
def CreateFDSign(data1, timeStamp):
    strContent = data1  + str(timeStamp) + fdsign
    return hashlib.md5(strContent.encode(encoding='UTF-8')).hexdigest()
def AddFDUserHeader(header):
    header["agent"] ="pc_client"
    header["version"] = "2.4.0"
    header["package"] = "com.fdzq.app"
    header["channel"] = "fdzq"
    header["Brand"] = "fdzq"
    header["device-id"] = "54-05-DB-50-C8-4A"
    header["Agent-Name"] = "Microsoft Windows 10"
    header["Device-Name"] = "DESKTOP-UQL3MEB"
    return header

def GetSizeInNiceString(sizeInBytes):
    """
    Convert the given byteCount into a string like: 9.9bytes/KB/MB/GB
    """
    for (cutoff, label) in [(1024*1024*1024, "GB"), (1024*1024, "MB"), (1024, "KB"),]:
        if sizeInBytes >= cutoff:
            return "%.1f %s" % (sizeInBytes * 1.0 / cutoff, label)
        if sizeInBytes == 1:
            return "1 byte"
        else:
            bytes = "%.1f" % (sizeInBytes or 0,)
    return (bytes[:-2] if bytes.endswith('.0') else bytes) + ' bytes'

def request(uri, method="GET", body=None, headers=None, redirections=5, connection_type=None,):
    http = httplib2.Http()
    starttime = int(round(time.time() * 1000))
    response, content = http.request(uri, method, body, headers,redirections,connection_type)
    finishTime = int(round(time.time() * 1000))
    return response, content, {"cost":  str(finishTime - starttime) +"ms", "len":GetSizeInNiceString(len(content))}
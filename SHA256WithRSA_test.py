from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

import base64

# 在线验证
# https://config.net.cn/tools/Sha256WithRSA-Sign.html

def lzSign(strMsg):
    # 加载私钥（PEM格式）
    with open("private.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,  # 如果私钥有密码，在此处输入
            backend=default_backend()
        )

    data = bytes(strMsg, 'utf-8')
    signature = private_key.sign(
        data,
        padding.PKCS1v15(),
        hashes.SHA256()
    )

    return signature


# 示例使用
if __name__ == "__main__":
    # # 加载私钥（PEM格式）
    # with open("private.pem", "rb") as key_file:
    #     private_key = serialization.load_pem_private_key(
    #         key_file.read(),
    #         password=None,  # 如果私钥有密码，在此处输入
    #         backend=default_backend()
    #     )
    #
    # # 需要签名的数据
    # data = b"xwfsfs"
    #
    # # 使用SHA256和PKCS#1 v1.5填充生成签名
    # signature = private_key.sign(
    #     data,
    #     padding.PKCS1v15(),
    #     hashes.SHA256()
    # )

    # 需要签名的数据
    # data = b"xwfsfs"
    strMsg = "xwfsfs"
    signature = lzSign(strMsg)

    print("Signature:", signature.hex())

    encoded_data = base64.b64encode(signature)
    print("Base64 编码结果:", encoded_data.decode("utf-8"))  # 转为字符串输出


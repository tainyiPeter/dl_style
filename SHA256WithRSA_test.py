from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

# # 生成密钥对
# private_key = rsa.generate_private_key(
#     public_exponent=65537,
#     key_size=2048,
#     backend=default_backend()
# )
# public_key = private_key.public_key()
#
#
# # 签名数据
# message = b"Hello, World!"
# signature = private_key.sign(
#     message,
#     padding.PSS(
#         mgf=padding.MGF1(hashes.SHA256()),
#         salt_length=padding.PSS.MAX_LENGTH
#     ),
#     hashes.SHA256()
# )

def en_private(message):
    # 生成密钥对
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    # 签名数据
    #message = b"Hello, World!"
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

def de_public(message):
    # 生成密钥对
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    plaintext = public_key.decrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext

if __name__ == '__main__':
    message = b"Hello, World!"
    abc = en_private(message)
    xyz = de_public(abc)
    print("xyz:", xyz)
    # # 生成密钥对
    # private_key = rsa.generate_private_key(
    #     public_exponent=65537,
    #     key_size=2048,
    #     backend=default_backend()
    # )
    # public_key = private_key.public_key()
    #
    #
    # # 签名数据
    # message = b"Hello, World!"
    # signature = private_key.sign(
    #     message,
    #     padding.PSS(
    #         mgf=padding.MGF1(hashes.SHA256()),
    #         salt_length=padding.PSS.MAX_LENGTH
    #     ),
    #     hashes.SHA256()
    # )
    #
    # signText = str(signature)
    # print("sign:", signText)
    # print("finish ...")
    #
    # # 验证签名
    # try:
    #     private_key.public_key().verify(
    #         signature,
    #         message,
    #         padding.PSS(
    #             mgf=padding.MGF1(hashes.SHA256()),
    #             salt_length=padding.PSS.MAX_LENGTH
    #         ),
    #         hashes.SHA256()
    #     )
    #     print("Signature is valid.")
    # except Exception as e:
    #     print("Signature is invalid.")
    #
    # # test
    # message123 = b"xxxx!"
    # # 公钥加密数据
    # ciphertext = public_key.encrypt(
    #     message123,
    #     padding.OAEP(
    #         mgf=padding.MGF1(algorithm=hashes.SHA256()),
    #         algorithm=hashes.SHA256(),
    #         label=None
    #     )
    # )
    #
    # # 私钥解密数据
    # plaintext = private_key.decrypt(
    #     ciphertext,
    #     padding.OAEP(
    #         mgf=padding.MGF1(algorithm=hashes.SHA256()),
    #         algorithm=hashes.SHA256(),
    #         label=None
    #     )
    # )
    # print("Decrypted message:", plaintext)  # 输出应为原始消息 b"Hello, World!"

    # # 假设你有一个字节串
    # binary_data = b'\xe4\xbd\xa0\xe5\xa5\xbd'  # 这是"你好"的UTF-8编码
    #
    # # 使用decode()方法转换为字符串
    # text = binary_data.decode('utf-8')
    # print(text)  # 输出: 你好
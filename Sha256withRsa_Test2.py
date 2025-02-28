from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.asymmetric.utils import (
    decode_dss_signature, encode_dss_signature
)

# 生成RSA密钥对
def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    return private_key, public_key

# 保存密钥到文件（可选）
def save_keys_to_file(private_key, public_key, private_file='private.pem', public_file='public.pem'):
    with open(private_file, 'wb') as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
    with open(public_file, 'wb') as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

# 从文件加载密钥（可选）
def load_keys_from_file(private_file='private.pem', public_file='public.pem'):
    with open(private_file, 'rb') as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None,
        )
    with open(public_file, 'rb') as f:
        public_key = serialization.load_pem_public_key(
            f.read()
        )
    return private_key, public_key

# 使用SHA256和RSA对消息进行签名
def sign_message(message, private_key):
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

# 验证签名
def verify_signature(message, signature, public_key):
    try:
        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception as e:
        return False



# 示例使用
if __name__ == "__main__":
    # 生成密钥对
    #private_key, public_key = generate_keys()

    # 可选：保存密钥到文件
    #save_keys_to_file(private_key, public_key)

    # 消息
    strMsg = "This is a secret message"
    bstrMsg = bytes(strMsg, 'utf-8')
    # message = bytes(strMsg, 'utf-8')
    message = b'This is a secret message'

    print(f"strMsg:{bstrMsg.hex()}")
    print(f"message:{message.hex()}")
    #
    # # 签名消息
    # signature = sign_message(message, private_key)
    # print("sign:", signature.hex())
    # print(f"Signature: {signature.hex()}")
    #
    # # 验证签名
    # bad_msg = b"esxfx"
    # # is_valid = verify_signature(message, signature, public_key)
    # is_valid = verify_signature(bad_msg, signature, public_key)
    # print(f"Signature valid: {is_valid}")
    #
    # 可选：从文件加载密钥并验证签名
    private_key, public_key = load_keys_from_file()
    # 签名消息
    signature = sign_message(message, private_key)
    print(f"sign: {signature.hex()}")

    sign2 = sign_message(message, private_key)
    print(f"sign: {sign2.hex()}")
    # is_loaded_valid = verify_signature(message, signature, public_key)
    # print(f"Signature valid after loading keys: {is_loaded_valid}")

import httplib2


def upload_file(url, file_path, token_auth, field_name='file', extra_fields=None):
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
        f'Content-Disposition: form-data; name="{field_name}"; filename="{file_path}"\r\n'.encode('utf-8')
    )
    body.append('Content-Type: application/octet-stream\r\n\r\n'.encode('utf-8'))

    # 读取文件内容（二进制模式）
    with open(file_path, 'rb') as f:
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



# 使用示例
if __name__ == '__main__':
    # 单个素材文件上传
    # response, content = upload_file(
    #     url= "https://cloud-biz.mbgtest.lenovomm.com/cloud-legionzone/file/uploadFile",
    #     token_auth="7b45ab30-ce13-4e26-8d09-898174486fc1",
    #     file_path='example.zip',
    #     extra_fields={'key': 'value'}
    # )

    # excel 文件上传
    response, content = upload_file(
        url= "https://cloud-biz.mbgtest.lenovomm.com/cloud-legionzone/biz/file/se/uploadFile",
        token_auth="a658d4fe-71ae-4f70-84ee-7089386e1de8",
        file_path='d:\\tmp\\ss.xlsx',
        extra_fields={'key': 'value'}
    )

    print(f'状态码: {response.status}')
    print(f'响应内容: {content.decode()}')
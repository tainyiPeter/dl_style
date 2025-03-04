import httplib2


def upload_file(url, file_path, field_name='file', extra_fields=None):
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
        'Authorization': 'bearer 7b45ab30-ce13-4e26-8d09-898174486fc1'
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
    # 上传文件并添加额外字段
    response, content = upload_file(
        # url='http://httpbin.org/post',
        url= "https://cloud-biz.mbgtest.lenovomm.com/cloud-legionzone/file/uploadFile",
        file_path='example.txt',
        extra_fields={'key': 'value'}
    )

    print(f'状态码: {response.status}')
    print(f'响应内容: {content.decode()}')
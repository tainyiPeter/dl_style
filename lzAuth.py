import httplib2
from urllib.parse import urlencode

# 请求的URL
url = 'https://cloud-pay.mbgtest.lenovomm.com/cloud-auth/oauth/token'

# 请求体数据
data = {
    "grant_type": "client_credentials",
    "client_id": "1593389727517312",
    "client_secret": "d248f803532a4d009c4bdecfb5bcd5cc"
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
print("Status Code:", response.status)
print("Response Content:", content.decode('utf-8'))
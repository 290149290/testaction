import requests

from requests.packages import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  #禁用CA警告

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0"}
headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1"}
s = requests.Session()  # 创建 requests.Session()对象s
s.headers = headers  # 集成了headers   #s.headers.update(headers)  # 另外种写法

url = 'https://webapi.sporttery.cn/gateway/lottery/getHistoryPageListV1.qry?gameNo=85&provinceId=0&pageSize=30&isVerify=1&pageNo=1'
url = 'https://webapi.sporttery.cn/gateway/lottery/getHistoryPageListV1.qry?gameNo=85&provinceId=0&pageSize=30&isVerify=1&pageNo=1'
r = s.get(url, verify=False, allow_redirects=False)  # 使用该对象s 进行get/post操作  # session已经包含了headers参数
# r = s.get(url, headers=headers, verify=False)  # 使用该对象s 进行get/post操作

print(r.text)

def save(file, res):
    with open(file, 'w', encoding='utf-8') as f:
        f.write(res)

# save("2020年12月7日_232100.txt", r.text)
# save("2020年12月8日.txt", r.json)
save("2020年12月8日.txt", r.text)
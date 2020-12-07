import requests

from requests.packages import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  #禁用CA警告

s = requests.Session()  # 创建 requests.Session()对象s
s.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0"}
# 集成header

# url = 'https://www.aaa.com'
url = 'https://webapi.sporttery.cn/gateway/lottery/getHistoryPageListV1.qry?gameNo=85&provinceId=0&pageSize=30&isVerify=1&pageNo=1'
r = s.get(url, verify=False)  # 使用该对象进行get/post操作  # session已经包含了headers参数 # 禁止ssl 解决https

print(r.text)

def save(file, res):
    with open(file, 'w', encoding='utf-8') as f:
        f.write(res)

save("2020年12月7日_232100.txt", r.text)
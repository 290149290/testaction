#作用：获取本地的外网出口地址
import requests
import re

def getIP():
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"
    response = requests.get('http://www.baidu.com/s?wd=ip',headers=headers)
    html = response.text
    reGET = re.compile('fk="(.*?)"').findall(html)
    for i in reGET:
        print('外网地址： %s'%i)
getIP()
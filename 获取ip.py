# 作用：获取本地的外网出口地址
import requests
import re


def getIP():
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"
    response = requests.get('http://www.baidu.com/s?wd=ip', headers=headers)
    html = response.text
    # reGET = re.compile('fk="(.*?)"').findall(html)
    # reGET = re.compile('ip地址(.*?) ').findall(html)
    reGET = re.compile('ip地址(.*?)。').findall(html)
    for i in reGET:
        print('外网地址： %s' % i)
        return i


ipinfo = getIP()


def save(file, res):
    with open(file, 'w', encoding='utf-8') as f:
        f.write(res)


def 时间_到文本(时间格式index=0, timetuple=None):
    '''

    :param 时间格式index:
    # 0 :  N年N月N日  示例:2020年11月20日
    # 1 :  N年N月N日N时N分N秒  示例:2020年11月20日4时25分38秒
    # 2 :  N年N月N日 N时N分N秒  示例:2020年11月20日 4时25分38秒
    # 3 :  年-月-日 时:分:秒  2020-11-20 4:25:38
    # 4 :  年/月/日 时/分/秒  2020/11/20 4/25/38
    :param timetuple:
        # 可传入 时间元组  如果不传 就默认取现行时间
    :return:
    '''
    # Done (2020年11月20日) 在版本3基础上 添加功能:时间格式 如果后续有需要 直接去list中添加对应格式
    # 时间格式index= ?
    # 0 :  N年N月N日  示例:2020年11月20日
    # 1 :  N年N月N日N时N分N秒  示例:2020年11月20日4时25分38秒
    # 2 :  N年N月N日 N时N分N秒  示例:2020年11月20日 4时25分38秒
    # 3 :  年-月-日 时:分:秒  2020-11-20 4:25:38
    # 4 :  年/月/日 时/分/秒  2020/11/20 4/25/38

    # def 时间_到文本(包含时分秒=False, timetuple=None):
    # 在版本2基础上 添加功能:支持传入 时间元组  如果不传 就默认取现行时间
    # struct_time  一般由time.localtime([secs])生成 参数secs省略就是取现行时间戳time.time()
    # struct_time 被提示重名了 改成了 timetuple

    import time
    # 检查到默认时间元组为None,那么就是取现行时间      # 如果没传入时间元组 就代表取现行时间
    if timetuple is None:
        timetuple = time.localtime()
    # time.struct_time(tm_year=2019, tm_mon=9, tm_mday=16, tm_hour=23, tm_min=45, tm_sec=13, tm_wday=0, tm_yday=259, tm_isdst=0)

    # 用*打散列表/元组等有序合集即可,需要几个参数它自己会传入个数,不会报错
    # N年N月N日 N时N分N秒  1=年-月-日 时:分:秒  2=年/月/日 时/分/秒  3=年月日时分秒
    # 时间格式index
    # 0 :  N年N月N日  示例:2020年11月20日
    # 1 :  N年N月N日N时N分N秒  示例:2020年11月20日4时25分38秒
    # 2 :  N年N月N日 N时N分N秒  示例:2020年11月20日 4时25分38秒
    # 3 :  年-月-日 时:分:秒  2020-11-20 4:25:38
    # 4 :  年/月/日 时/分/秒  2020/11/20 4/25/38
    result_list = [
        "{}年{}月{}日",
        "{}年{}月{}日{}时{}分{}秒",
        "{}年{}月{}日 {}时{}分{}秒",
        "{}-{}-{} {}:{}:{}",
        "{}/{}/{} {}/{}/{}",
    ]

    return result_list[时间格式index].format(*timetuple)


file = 时间_到文本(时间格式index=1) + ".txt"
save(file, ipinfo)

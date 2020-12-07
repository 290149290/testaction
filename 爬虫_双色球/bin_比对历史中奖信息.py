# ' --------------------------+---------------------------- '
# 1. 解决cmd命令下无法 正确导入同文件夹下 .py模块
# 2. pycharm中 直接将父目录 右键 标记文件夹为root  就是mark directory as Root
import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
print(curPath)
sys.path.append(curPath)
rootPath = os.path.split(curPath)[0]
print(rootPath)
sys.path.append(rootPath)
# ' --------------------------+---------------------------- '
from 爬虫_双色球.liukai import *
import time
# ' --------------------------+---------------------------- '#GET
import urllib.request
import http.cookiejar
import urllib.parse

# 获得cookie管理器
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "utf-8",
    "Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0"
}


def get(url):
    # 构造req 包含url,header信息的对象
    req = urllib.request.Request(url, headers=header)
    # res = opener.open(req).read().decode()
    # res = opener.open(req,timeout=10).read().decode()

    try:
        res = opener.open(req, timeout=10).read().decode()
        return res
    except:
        # save("error.txt","url异常")
        print("error", url)
        # file="error.txt"
        # with open(file, 'a+', encoding='utf-8') as f:
        #     f.write(url+"\n")

        return None


def save(file, res):
    with open(file, 'w', encoding='utf-8') as f:
        f.write(res)


def 首页_下载(url, file):
    while True:
        res = get(url)
        if res != None:
            save(file, res)
            break
        else:
            print(url, "下载失败")

        time.sleep(2.5)
        print("正在重试", url)


def 首页_解析(file, result_file):
    # res = 文件_读入文本("page1.txt")
    res = 文件_读入文本(file)

    final_lis = []
    # ' --------------------------+---------------------------- 'url
    final_lis.append(首页_url)  # url
    # ' --------------------------+---------------------------- '■小说标题 作者简介
    temp_list = result_作者简介_部分(res)
    final_lis.extend(temp_list)
    # ' --------------------------+---------------------------- '■开始 章节目录处理
    temp_list = result_章节目录_部分(res)
    final_lis.extend(temp_list)
    # ' --------------------------+---------------------------- '
    final = "\n".join(final_lis)
    save(result_file, final)  # 写1次文件 查看下用的
    return


def result_作者简介_部分(res):
    # 取1次文本
    前面文本 = '<div class="book-describe">'
    后面文本 = '</div>'
    res = 文本_取中间文本(res, 前面文本, 后面文本)
    # print(res)

    # title
    前面文本 = "<h1>"
    后面文本 = "</h1>"
    title = 文本_取中间文本(res, 前面文本, 后面文本)

    前面文本 = "<p>"
    后面文本 = "</p>"
    lis = 文本_取中间_批量(res, 前面文本, 后面文本)
    result_lis = []  # lis要处理  处理的结果存放于 result_lis
    for i in lis:
        if "最近更新" in i: continue
        if "最新章节" in i: continue
        if "电梯直达" in i: break
        result_lis.append(i)

    final_lis = []
    # final_lis.append(首页_url)  # url
    final_lis.append(title)  # tile 小说标题
    final_lis.extend(result_lis)  # 作者 简介 这些
    # final = "\n".join(final_lis)
    # save(result_file,final)   #写1次文件 查看下用的
    return final_lis


def result_h3章节(txt):
    # h3章节格式  title="蛮荒记5九鼎" href="https://www.luoxia.com/manhuangji/mhj-5/"
    前面文本 = 'title="'
    后面文本 = '"'
    title = 文本_取中间文本(txt, 前面文本, 后面文本)
    title = title.rstrip()

    前面文本 = 'href="'
    href = 文本_取中间文本(txt, 前面文本, 后面文本)

    # if title == None or href == None:
    # print("None", txt)
    # breakpoint()
    return title + "," + href


def result_子章节(txt):
    result_list = []

    # 子章节格式 <a target="_blank" title="第一章 青青子衿 · 1" href="https://www.luoxia.com/manhuangji/95656.htm">第一章 青青子衿 · 1</a>
    前面文本 = '<a '
    后面文本 = '</a>'
    # lis = 文本_取中间文本(txt, 前面文本, 后面文本)
    lis = 文本_取中间_批量(txt, 前面文本, 后面文本)
    print(lis)
    for i in lis:
        # 因为取文本格式 与 xx 一样 所以直接调用
        result = result_h3章节(i)
        result_list.append(result)

    return result_list


def result_章节目录_部分(res):
    final_lis = []

    前面文本 = "</h2>"
    后面文本 = '<div id="lxfoot" class="copyright bt clearfix">'
    章节目录文本 = 文本_取中间文本(res, 前面文本, 后面文本)

    前面文本 = "<div class="
    后面文本 = "</div>"
    章节目录_list = 文本_取中间_批量(章节目录文本, 前面文本, 后面文本)
    print(章节目录_list)

    for i in 章节目录_list:
        if "title clearfix" in i:  # 按 h3章节标题取  得到是 文本
            temp = result_h3章节(i)
            print(temp, "= result_h3章节(i)")
            final_lis.append(temp)

        if "book-list clearfix" in i:  # 按子章节取  得到的是个list
            temp_list = result_子章节(i)
            print(temp_list, "= result_子章节(i)")
            final_lis.extend(temp_list)  # 作者 简介 啥的

    return final_lis


def 首页_解析结果_downurl(file, 小说_url_拼音):
    res = 文件_读入文本(file)
    lis = res.split("\n")

    # all_list =[]
    error_list = []  # 设置一个列表 记录 下载异常的文件
    done_list = []  # 记录 下载成功的文件
    while True:

        for i in lis:
            if "https://www.luoxia.com/" in i and ".htm" in i:  # if ".htm" in i:

                # if i not in all_list:  #
                #     all_list.append(i)

                if i in done_list:  # 如果这行下载过 就不再下了
                    continue

                # 第一章 婚礼前夕 · 1,https://www.luoxia.com/manhuangji/95480.htm
                前面文本 = "https://www.luoxia.com/{}/".format(小说_url_拼音)
                number = 文本_取中间文本(i, 前面文本, ".htm")
                url = "https://www.luoxia.com/{}/{}.htm".format(小说_url_拼音, number)

                file = "{}.htm".format(number)
                if 文件_是否存在(file): continue  # 要保存的文件如果存在 就到循环尾 //不下载了

                # 开始下载
                res = get(url)
                time.sleep(2.5)  # 每个下载 延时2.5秒

                if res == None:
                    pass
                    print(i, "下载异常")
                    # ■这里异常了 超时了 或者其他
                    if i not in error_list:
                        error_list.append(i)

                else:
                    save(file, res)

                    if i not in done_list:  # 下载成功 添加进下载完毕列表
                        done_list.append(i)

                    if i in error_list:  # 下载成功 从错误列表中移出
                        error_list.remove(i)

        print("error_list", error_list)

        # 如果错误列表为空  就表示下载完了
        if error_list == []:
            print("错误列表为空,将退出循环")
            break


def all_htm_to_txt(file, 小说_url_拼音):
    res = 文件_读入文本(file)
    lis = res.split("\n")

    for i in lis:
        if "https://www.luoxia.com/" in i and ".htm" in i:  # if ".htm" in i:
            # 第一章 婚礼前夕 · 1,https://www.luoxia.com/manhuangji/95480.htm
            # number = 文本_取中间文本(i, "https://www.luoxia.com/manhuangji/", ".htm")
            # url = "https://www.luoxia.com/manhuangji/{}.htm".format(number)
            前面文本 = "https://www.luoxia.com/{}/".format(小说_url_拼音)
            number = 文本_取中间文本(i, 前面文本, ".htm")

            file_htm = "{}.htm".format(number)
            file_txt = "{}.txt".format(number)
            if 文件_是否存在(file_htm) != True:
                print("error,htm文件并不存在", file_htm)
                continue
            if 文件_是否存在(file_txt):
                continue
            # 开始 解析htm文件
            htm = 文件_读入文本(file_htm)
            txt = htm_to_txt(htm)

            save(file=file_txt, res=txt)


def htm_to_txt(htm):
    txt_list = []  # 存放最终文本 列表
    # ' --------------------------+---------------------------- ' #取标题
    前面文本 = '"post-title">'
    后面文本 = '</h1>'
    title = 文本_取中间文本(htm, 前面文本, 后面文本)
    txt_list.append(title)
    # ' --------------------------+---------------------------- '取正文 并处理 行首缩进
    前面文本 = '<div id="nr1">'
    后面文本 = '</div>'
    content = 文本_取中间文本(htm, 前面文本, 后面文本)
    前面文本 = '<p>'
    后面文本 = '</p>'
    content_list = 文本_取中间_批量(content, 前面文本, 后面文本)
    # print(len(content_list))

    for i in content_list:
        temp = "    " + i
        txt_list.append(temp)
    # ' --------------------------+---------------------------- '\n换行符连接
    # print(len(txt_list))
    txt = "\n".join(txt_list)
    return txt


def all_txt_join(目录file, 保存文件file, 小说_url_拼音):
    res = 文件_读入文本(目录file)
    lis = res.split("\n")

    all_txt_list = []

    for i in lis:
        if "https://www.luoxia.com/" in i and ".htm" in i:  # if ".htm" in i:
            # 第一章 婚礼前夕 · 1,https://www.luoxia.com/manhuangji/95480.htm
            # number = 文本_取中间文本(i, "https://www.luoxia.com/manhuangji/", ".htm")
            前面文本 = "https://www.luoxia.com/{}/".format(小说_url_拼音)
            number = 文本_取中间文本(i, 前面文本, ".htm")
            file_txt = "{}.txt".format(number)

            if 文件_是否存在(file_txt) != True:
                print("error,htm文件并不存在", file_txt)
                continue
            # 开始 解析htm文件
            txt = 文件_读入文本(file_txt)
            txt = "\n" + txt  # ■细节处理 每个章节前面都要空一行
            txt = "\n" + txt  # ■再空一行
            all_txt_list.append(txt)

        else:
            # 除了htm关键字所在的文本 其余都最终要写到all_txt里面的
            all_txt_list.append(i)

    all_txt = "\n".join(all_txt_list)
    # save(file="树下野狐_蛮荒记.txt", res=all_txt)
    save(file=保存文件file, res=all_txt)


def 首页_解析_返回小说文件名(首页_url_file):
    # '''<h1>兄弟</h1>  <p>作者：余华</p>'''
    文本 = 文件_读入文本(首页_url_file)
    标题 = 文本_取中间文本(文本, '<h1>', '</h1>')
    作者 = 文本_取中间文本(文本, '<p>作者：', '</p>')
    return 作者 + "_" + 标题 + ".txt"  # 小说_txt = "余华_兄弟.txt"


def 首页_url_自动适配输入格式(url):
    # ■正常的url格式
    if "https://www.luoxia.com/" in url:
        # return url
        return url.strip()  # 去除首尾空

    # ■小说拼音
    if "/" not in url:
        return "https://www.luoxia.com/{}/".format(url)


# ■□下载所有页
def down_all_url(首页file):
    # http://kaijiang.zhcw.com/zhcw/html/ssq/list_1.html

    # http://kaijiang.zhcw.com/zhcw/html/ssq/list_2.html
    # ...
    # http://kaijiang.zhcw.com/zhcw/html/ssq/list_130.html
    res = 文件_读入文本(首页file)
    pageMax = 文本_取中间文本(res, "共<strong>", "</strong>")
    print(pageMax)  # 130
    pageMax = int(pageMax)

    error_list = []  # 设置一个列表 记录 下载异常的文件
    done_list = []  # 记录 下载成功的文件

    while True:  # 这里循环是 处理 下载超时/下载失败的url
        for i in range(1, pageMax + 1):  # 2~130  因为第1页下载过了
            if i in done_list: continue  # ■如果这行下载过 就不再下了
            url = "http://kaijiang.zhcw.com/zhcw/html/ssq/list_{}.html".format(i)
            file = "{}.html".format(i)  # 130.html
            if 文件_是否存在(file): continue  # ■ 要保存的文件如果存在 就到循环尾 //不下载了

            # 开始下载
            res = get(url)
            time.sleep(2.5)  # 每个下载 延时2.5秒

            if res == None:
                print(i, "下载异常")
                # ■这里异常了 超时了 或者其他
                if i not in error_list:
                    error_list.append(i)

            else:
                save(file, res)

                if i not in done_list:  # 下载成功 添加进下载完毕列表
                    done_list.append(i)

                if i in error_list:  # 下载成功 从错误列表中移出
                    error_list.remove(i)

        print("error_list", error_list)

        # 如果错误列表为空  就表示下载完了
        if error_list == []:
            print("错误列表为空,将退出循环")
            break


def 单个_html_解析(file):
    res = 文件_读入文本(file)
    前面 = "<tr>"
    后面 = "开奖视频"
    lis = 文本_取中间_批量(res, 前面, 后面)

    result_list = []
    for i in lis:
        result = 单个_项目_解析(i)
        result_list.append(result)

    return result_list


def 单个_项目_解析(i):
    # <td align="center">2020-07-26</td>
    前面 = '<td align="center">'
    后面 = "</td>"
    lis = 文本_取中间_批量(i, 前面, 后面)
    开奖日期 = lis[0]
    开奖期号 = lis[1]

    # <em class="rr">12</em>
    前面 = '<em class="rr">'
    后面 = "</em>"
    红球_lis = 文本_取中间_批量(i, 前面, 后面)
    # <em>10</em></td>
    前面 = '<em>'
    后面 = "</em>"
    蓝球 = 文本_取中间文本(i, 前面, 后面)
    开奖号码 = ",".join(红球_lis) + "," + 蓝球

    lis = [开奖日期, 开奖期号, 开奖号码]
    return "\t".join(lis)


def 所有_html_解析(首页file):
    res = 文件_读入文本(首页file)
    pageMax = 文本_取中间文本(res, "共<strong>", "</strong>")
    print(pageMax)  # 130
    pageMax = int(pageMax)

    lis = []
    for i in range(1, pageMax + 1):  # 2~130  因为第1页下载过了
        file = "{}.html".format(i)  # 130.html
        # if 文件_是否存在(file): continue  # ■ 要保存的文件如果存在 就到循环尾 //不下载了
        temp_lis = 单个_html_解析(file)  # 返回的是个list  20组数据左右
        lis.extend(temp_lis)

    txt = "\n".join(lis)
    file = "all.txt"
    # 覆盖式写入
    with open(file, 'w', encoding='utf-8') as f:
        f.write(txt)


def 文件写入_sqlite(file='all.txt'):
    import sqlite3

    conn = sqlite3.connect('ssq.db')
    c = conn.cursor()
    print("Opened database successfully")

    txt = 文件_读入文本(file)
    lis = txt.split("\n")
    for i in lis:
        temp_list = i.split("\t")
        开奖日期, 期号, 号码 = temp_list
        # c.execute("INSERT INTO ssq (开奖日期,期号,号码) VALUES ('1', '2', 'California')");
        c.execute("INSERT INTO ssq (开奖日期,期号,号码) VALUES ('{}', '{}', '{}')".format(开奖日期, 期号, 号码));

    conn.commit()  # 一次性提交事务
    print("Records created successfully")
    conn.close()


def 查询_写入(file='all.txt'):
    import sqlite3

    conn = sqlite3.connect('ssq.db')
    c = conn.cursor()
    print("Opened database successfully")

    # cursor = c.execute("SELECT 开奖日期, 期号, 号码  from ssq")
    # cursor = c.execute("SELECT 期号 from ssq")
    # print(cursor)  # <sqlite3.Cursor object at 0x0273D9A0>
    #
    # # for row in cursor:  #元组
    # # print(row)    #只有1个查询结果时  期数  ('2020085',)  #cursor = c.execute("SELECT 期号 from ssq")
    # # print("期号 = ", row[0]) # cursor = c.execute("SELECT 开奖日期, 期号, 号码  from ssq")
    # # print("开奖日期 = ", row[0])
    # # print("期号 = ", row[1])
    # # print("号码 = ", row[2] , "\n")
    # # print("SALARY = ", row[3], "\n")
    # print('2020083' in cursor)  # False
    # print(('2020083',) in cursor)  # False
    #
    # conn.commit()  # 一次性提交事务
    # print("Records created successfully")
    # conn.close()
    #
    # return

    txt = 文件_读入文本(file)
    lis = txt.split("\n")
    for i in lis:
        temp_list = i.split("\t")
        开奖日期, 期号, 号码 = temp_list
        # c.execute("INSERT INTO ssq (开奖日期,期号,号码) VALUES ('1', '2', 'California')");

        # cursor = c.execute("SELECT id, name, address, salary  from COMPANY")
        # cursor = c.execute("SELECT 开奖日期, 期号, 号码  from ssq")
        # sql语句 = "select * from ssq where 开奖日期='{}' and 期号='{}' and 号码='{}'".format(开奖日期, 期号, 号码)
        sql语句 = "select COUNT(*) from ssq where 开奖日期='{}' and 期号='{}' and 号码='{}'".format(开奖日期, 期号, 号码)
        # sql语句 = "select COUNT(*) from (ssq where 开奖日期='{}' and 期号='{}' and 号码='{}') a".format(开奖日期, 期号, 号码)
        # select count(*) from (select ... from ... where ...) as a

        # sql语句 = "select COUNT(1) from ssq where 开奖日期='{}' and 期号='{}' and 号码='{}'".format(开奖日期, 期号, 号码)
        cursor = c.execute(sql语句)
        number = cursor.fetchone()[0]  #cursor.fetchone()结果是(4,)这样一个元组 取出来就是了
        print(cursor,number)

        # print(number,"记录条数")
        if number > 1:
            print("已经重复存在,即将删除", 开奖日期, 期号, 号码)
            sql语句 = "DELETE from ssq where 开奖日期='{}' and 期号='{}' and 号码='{}'".format(开奖日期, 期号, 号码)
            c.execute(sql语句)
        elif number ==1:
            print("已经存在")
        elif number ==0:
            print("即将添加")
            sql语句 = "INSERT INTO ssq (开奖日期,期号,号码) VALUES ('{}', '{}', '{}')".format(开奖日期, 期号, 号码)
            c.execute(sql语句)
            # c.execute("INSERT INTO ssq (开奖日期,期号,号码) VALUES ('{}', '{}', '{}')".format(开奖日期, 期号, 号码))
        # break  # 调试用

    conn.commit()  # 一次性提交事务
    print("Records created successfully")
    conn.close()

def 彩票_查询彩票结果(开奖日期, 开奖期号, 开奖结果):
    # def 彩票_查询彩票结果(开奖结果):
    # '双色球 ssq
    # 开奖结果 = 双色球_取开奖结果_zhcw()
    自选号码_数组 = []
    自选号码_数组.append("01,05,06,14,22,29,03")
    自选号码_数组.append("03,05,06,14,23,29,08")
    自选号码_数组.append("03,04,06,07,08,30,06")
    # #
    自选号码_数组.append("01,04,06,11,30,31,11")
    # #
    自选号码_数组.append("03,04,05,06,12,33,04")
    自选号码_数组.append("03,04,05,06,12,33,06")
    # print('自选号码_数组',自选号码_数组)

    # Flag_是否中奖 = False

    for i in range(len(自选号码_数组)):
        对比结果 = 彩票_号码对比(开奖结果, 自选号码_数组[i], 0,开奖日期,开奖期号)
        # print(对比结果)
        lis = ["一等奖","二等奖","三等奖","四等奖"]
        # if 对比结果[1] != "":  # 对比结果没中奖是空文本
        if 对比结果[1] in lis:  # 对比结果
            # Flag_是否中奖 = True
            print(对比结果)

    # print("' --------------------------+---------------------------- '")


def 彩票_取中奖等级(彩票类型: 'int <= 1', 红球_出现次数: '0 <= int <= 6', 蓝球_出现次数: '0 <= int <= 2'):  # 0是双色球 1是大乐透

    # tod 优化3:限制参数的值和类型
    # tod 优化1:改为字典类型 将逻辑与数据剥离开
    # tod 优化2:因为同时只用得到1个字典 不必用list [0] 和 [1] 才同时存放2个字典
    #  if 彩票类型: dic=  ... 双色球那部分  else dic= ...大乐透那部分
    #  return dic[兑奖结果]  if 兑奖结果 in dic:  else ""

    # 彩票类型别超过显示了 0~1
    if 彩票类型 > 1:
        msg = input("彩票类型超限,0是双色球,1是大乐透,请输入0或者1继续!")
        print(msg)
        if msg in ["0", "1"]:
            彩票类型 = int(msg)
            print("彩票类型", 彩票类型)

    # todo 彩票类型如果为双色球,红球6/蓝球1 数量不能超过上限
    #     彩票类型如果为大乐透,红球5/蓝球2 数量不能超过上限

    # 中奖等级 字典#0是双色球 1是大乐透
    dic = {}
    if 彩票类型 == 0:
        # 双色球中奖等级 字典
        dic = {
            "6,1": "一等奖",
            "6,0": "二等奖",
            "5,1": "三等奖",
            "5,0": "四等奖",
            "4,1": "四等奖",
            "4,0": "五等奖",
            "3,1": "五等奖",
            "2,1": "六等奖",
            "1,1": "六等奖",
            "0,1": "六等奖",
        }
    elif 彩票类型 == 1:
        # 大乐透 中奖等级 字典
        dic = {
            "5,2": "一等奖",
            "5,1": "二等奖",
            "5,0": "三等奖",
            "4,2": "四等奖",
            "4,1": "五等奖",
            "3,2": "六等奖",
            "4,0": "七等奖",
            "3,1": "八等奖",
            "2,2": "八等奖",
            "3,0": "九等奖",
            "2,1": "九等奖",
            "1,2": "九等奖",
            "0,2": "九等奖",
        }

    # print("here")

    兑奖结果 = str(红球_出现次数) + ',' + str(蓝球_出现次数)  # 格式:'0,0'  '0,1'

    return dic[兑奖结果] if 兑奖结果 in dic else ""  # 当'0,0' 不在中奖等级里面 如果直接取 就会keyError 因此要判断:if 兑奖结果 in dic
    # if 兑奖结果 in dic:
    #     return dic[兑奖结果]
    # else:
    #     return""

    # todo:2:如果没中奖 不用暂停等人工输入y,直接走  中奖了播放百度合成的那个声音


def 彩票_号码对比(开奖号码, 自选号码, 彩票类型,开奖日期,开奖期号):  # 0是双色球 1是大乐透
# def 彩票_号码对比(开奖号码, 自选号码, 彩票类型):  # 0是双色球 1是大乐透

    彩票_种类 = ""
    红球个数 = 0
    if 彩票类型 == 0:
        彩票_种类 = '双色球'
        红球个数 = 6
    if 彩票类型 == 1:
        彩票_种类 = '大乐透'
        红球个数 = 5

    蓝球个数 = 7 - 红球个数

    # 截取 左边部分   双色球 红球就是 [0:14] 也可以写成[:14]
    ##错了  会少一位  红球_文本 = 开奖号码[0:(红球个数 * 2 + (红球个数 -1) * 1)-1]  # 5个号码+4个逗号=5*2+4*1 =14  #python里面是第一位索引是0,所以要-1 错了 末尾标识位置的不会包含
    红球_文本 = 开奖号码[0:(红球个数 * 2 + (红球个数 - 1) * 1)]  # 5个号码+4个逗号=5*2+4*1 =14  #python里面是第一位索引是0,所以要-1 错了 末尾标识位置的不会包含

    # 截取_右边部分   双色球 蓝球就是 [-2:]  也可以写成[-2:-1]  #这里犯错了[-2:] 和[-2:-1] 是不一样的
    ####写错了蓝球_文本 = 开奖号码[(0-(蓝球个数 * 2 + (蓝球个数-1) * 1)):-1]
    蓝球_文本 = 开奖号码[(0 - (蓝球个数 * 2 + (蓝球个数 - 1) * 1)):]

    自选号码_数组 = 自选号码.split(',')

    红球_出现数组 = []
    红球_出现次数 = 0
    for i in range(红球个数):
        if 红球_文本.find(自选号码_数组[i]) > -1:  # 自选号码里面的每个成员 拿去 在 红球_文本 中寻找 是否出现
            红球_出现次数 = 红球_出现次数 + 1
            红球_出现数组.append(自选号码_数组[i])

    蓝球_出现数组 = []
    蓝球_出现次数 = 0
    for i in range(蓝球个数):
        # 自选号码里面的每个成员 拿去 在 蓝球_文本 中寻找 是否出现
        # 因为前面有红球 所以 成员起始比较 要从第一个蓝球开始 就是红球后面
        if 蓝球_文本.find(自选号码_数组[i + 红球个数]) > -1:
            蓝球_出现次数 = 蓝球_出现次数 + 1
            蓝球_出现数组.append(自选号码_数组[i + 红球个数])

    # 红球_出现文本 = 数组_到文本(红球_出现数组)
    红球_出现文本 = ','.join(红球_出现数组)
    蓝球_出现文本 = ','.join(蓝球_出现数组)
    # 蓝球_出现文本 = 数组_到文本(蓝球_出现数组)

    中奖结果 = 彩票_取中奖等级(彩票类型, 红球_出现次数, 蓝球_出现次数)

    if 中奖结果 == '一等奖':
        ...
        # playsound(r'D:\快盘\code_POST\POST_有利\铃声.wav')
        # playsound(r'D:\快盘\code_签到\DOTA_firstblood.mp3')

    return (彩票_种类 + '|' +
            '自选号码:' + 自选号码 + '|' +
            '开奖号码:' + 开奖号码 + '|' +
            '红球' + 红球_出现文本 +
            ',蓝球' + 蓝球_出现文本 +
            ',匹配:,' + str(红球_出现次数) + '+' + str(蓝球_出现次数) + '|' + '奖项:' + 中奖结果
            , 中奖结果,"开奖日期:"+开奖日期+"|"+"开奖期号:"+开奖期号)
    # 2019年11月21日  新增 返回 元组的元素  中奖结果  #目的是 当未中奖时,该内容为空,不需要给用户显示

def 数据库_取开奖号码_对比历史中奖等级():
    import sqlite3

    conn = sqlite3.connect('ssq.db')
    c = conn.cursor()
    print("Opened database successfully")
    # ' --------------------------+---------------------------- '
    sql语句= "select * from ssq"
    lis = c.execute(sql语句)
    for i in lis:
        开奖日期=i[0]
        期数=i[1]
        号码=i[2]
        # 彩票_查询彩票结果(号码)
        彩票_查询彩票结果(开奖日期=i[0],开奖期号=i[1],开奖结果=i[2])



    # ' --------------------------+---------------------------- '
    conn.commit()
    print("Records created successfully")
    conn.close()

def 测试写入():
    import sqlite3

    conn = sqlite3.connect('ssq.db')
    c = conn.cursor()
    print("Opened database successfully")

    # c.execute("INSERT INTO ssq (开奖日期,期号,号码) VALUES ('1', '2', 'California')");
    #
    # c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
    #       VALUES (2, 'Allen', 25, 'Texas', 15000.00 )");
    #
    # c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
    #       VALUES (3, 'Teddy', 23, 'Norway', 20000.00 )");
    #
    # c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
    #       VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 )");

    conn.commit()
    print("Records created successfully")
    conn.close()


# 首页
# url = "http://kaijiang.zhcw.com/zhcw/html/ssq/list.html"
# url = "http://kaijiang.zhcw.com/zhcw/html/ssq/list_1.html"  # 首页 也可以是这种
# 首页file = "1.html"
# ' --------------------------+---------------------------- '下载
# 首页_下载(url=url, file=首页file)  # ■下载与解析分离
# down_all_url(首页file)
# ' --------------------------+---------------------------- ' 解析
# 所有_html_解析(首页file)
# ' --------------------------+---------------------------- '
# 文件写入_sqlite()
# 查询_写入()
if __name__ == '__main__':
    t = time.time()

    # 查询_写入()
    数据库_取开奖号码_对比历史中奖等级()


    print("耗时", time.time() - t)

'''
.版本 2
.支持库 spec
pageMax ＝ 到整数 (文本_取出中间文本 (res, “共<strong>”, “</strong>”, , ))
调试输出 (“pageMax”, pageMax)

'''

exit()
#
# # ' --------------------------+---------------------------- '# ■只需要1个参数 url或者书名  # 代码自动适配url,书名,去首尾空
# # 首页_url = "https://www.luoxia.com/xiongdi/"   #
# 首页_url = "santi"  # 输入url也可以
# 首页_url = "https://www.luoxia.com/weicheng/"  # 输入url也可以
#
# # ' --------------------------+---------------------------- ''# 代码  包括一些自动适配或默认的参数
# 首页_url = 首页_url_自动适配输入格式(首页_url)
# 首页_url_file = "page.txt"
# 首页_解析结果_file = "page_result.txt"
# 小说_url_拼音 = 文本_取中间文本(首页_url, "https://www.luoxia.com/", "/")
# # ' --------------------------+----------------------------
# 首页_下载(url=首页_url, file=首页_url_file)  # ■下载与解析分离
# 首页_解析(file=首页_url_file, result_file=首页_解析结果_file)  # ■解析的文件 存放
# 首页_解析结果_downurl(file=首页_解析结果_file, 小说_url_拼音=小说_url_拼音)  # ■下载 目标url  htm
# all_htm_to_txt(file=首页_解析结果_file, 小说_url_拼音=小说_url_拼音)  # ■ 下载的url文件 htm内容需要转换为txt
# 小说_txt = 首页_解析_返回小说文件名(首页_url_file)  # ■自动生成小说名称 #小说_txt = "余华_兄弟.txt"
# all_txt_join(目录file=首页_解析结果_file, 保存文件file=小说_txt, 小说_url_拼音=小说_url_拼音)  # ■ 下载的url文件 htm内容需要转换为txt
#
# # ' --------------------------+---------------------------- '
# print("done")  # ■这个提示是必要的

# ■读取 首页url
# ■提取期号 号码等数据
# ■判断 当前页的全部期号 及 号码 是否存在于数据库  ■存在就跳出循环  不存在就加入
#   ■都不存在 就继续 get_url
#   ■如果是最后一页  也不继续get_url了


from liukai import *
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


def get_首页(url):
    while True:
        res = get(url)

        time.sleep(2.5)  # ■每个get url 后面加点延时

        if res != None:
            # save(file, res)
            return res
        else:
            print(url, "下载失败")
            print("正在重试", url)

        # ■□放在这里是错误的 因为上面直接return了
        # time.sleep(2.5)  # ■每个get url 后面加点延时


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
    # 期号
    # bgcolor="#f9f9f9">20085</td>
    # 前面 = 'bgcolor'
    # 后面 = "/td>"
    开奖期号 = 文本_取中间文本(i, 'bgcolor', "/td>")  # 粗筛关键文本
    # 前面 = '>'
    # 后面 = "<"
    开奖期号 = 文本_取中间文本(开奖期号, '>', "<")  # 取到

    # 开奖日期
    # 前面 = 'bgcolor'
    # 后面 = "/td>"
    文本_lis = 文本_取中间_批量(i, 'bgcolor', "/td>")  # 粗筛关键文本
    开奖日期 = 文本_lis[-1]
    开奖日期 = 文本_取中间文本(开奖日期, '>', "<")  # 取到

    # 红球lis  #"red">02</td>
    红球_lis = 文本_取中间_批量(i, '"red">', '</td>')  # 粗筛关键文本
    # 蓝球lis  #class="blue">06</td>
    蓝球_lis = 文本_取中间_批量(i, '"blue">', '</td>')  # 粗筛关键文本
    # 开奖号码
    开奖号码_lis = []
    开奖号码_lis.extend(红球_lis)
    开奖号码_lis.extend(蓝球_lis)
    开奖号码 = ','.join(开奖号码_lis)

    lis = [开奖日期, 开奖期号, 开奖号码]
    return "\t".join(lis)


def 解析_首页(res):
    前面 = "<tbody>"
    后面 = "</tbody>"
    res = 文本_取中间文本(res, 前面, 后面)

    前面 = "<tr>"
    后面 = "</tr>"
    lis = 文本_取中间_批量(res, 前面, 后面)
    关键文本 = '<td align="center"'  # 20个项目 实际有多余的无关项目   //关键字 red blue 也行
    result_list = []
    for i in lis:
        if 关键文本 in i:
            result = 单个_项目_解析(i)
            result_list.append(result)

    return result_list


def 对比_sqlite数据库(lis):
    import sqlite3

    # conn = sqlite3.connect('ssq.db')
    conn = sqlite3.connect('dlt.db')
    c = conn.cursor()
    # print("Opened database successfully")

    number_new = 0  # 新加入的数据数量
    for i in lis:
        temp_list = i.split("\t")
        开奖日期, 期号, 号码 = temp_list
        # c.execute("INSERT INTO ssq (开奖日期,期号,号码) VALUES ('1', '2', 'California')");
        # cursor = c.execute("SELECT id, name, address, salary  from COMPANY")
        # cursor = c.execute("SELECT 开奖日期, 期号, 号码  from ssq")
        # sql语句 = "select * from ssq where 开奖日期='{}' and 期号='{}' and 号码='{}'".format(开奖日期, 期号, 号码)
        # sql语句 = "select COUNT(*) from ssq where 开奖日期='{}' and 期号='{}' and 号码='{}'".format(开奖日期, 期号, 号码)
        sql语句 = "select COUNT(*) from dlt where 开奖日期='{}' and 期号='{}' and 号码='{}'".format(开奖日期, 期号, 号码)
        # sql语句 = "select COUNT(*) from (ssq where 开奖日期='{}' and 期号='{}' and 号码='{}') a".format(开奖日期, 期号, 号码)
        # select count(*) from (select ... from ... where ...) as a

        # sql语句 = "select COUNT(1) from ssq where 开奖日期='{}' and 期号='{}' and 号码='{}'".format(开奖日期, 期号, 号码)
        cursor = c.execute(sql语句)
        number = cursor.fetchone()[0]  # cursor.fetchone()结果是(4,)这样一个元组 取出来就是了
        print(cursor, number)

        # print(number,"记录条数")
        if number > 1:
            print("已经重复存在,即将删除", 开奖日期, 期号, 号码)
            # sql语句 = "DELETE from ssq where 开奖日期='{}' and 期号='{}' and 号码='{}'".format(开奖日期, 期号, 号码)
            sql语句 = "DELETE from dlt where 开奖日期='{}' and 期号='{}' and 号码='{}'".format(开奖日期, 期号, 号码)
            c.execute(sql语句)
        elif number == 1:
            print("已经存在", i)
        elif number == 0:
            print("即将添加",开奖日期, 期号, 号码)
            # sql语句 = "INSERT INTO ssq (开奖日期,期号,号码) VALUES ('{}', '{}', '{}')".format(开奖日期, 期号, 号码)
            sql语句 = "INSERT INTO dlt (开奖日期,期号,号码) VALUES ('{}', '{}', '{}')".format(开奖日期, 期号, 号码)
            c.execute(sql语句)
            # c.execute("INSERT INTO ssq (开奖日期,期号,号码) VALUES ('{}', '{}', '{}')".format(开奖日期, 期号, 号码))
            number_new = number_new + 1  # ■新加入的数据数量
        # break  # 调试用

    conn.commit()  # 一次性提交事务
    print("Records created successfully")
    conn.close()

    if number_new == len(lis):  # ■□ 当前页面都是新加入的数据数量
        return True
    else:
        return False


def creat_sqlite(db, table, row1, row2, row3):
    import sqlite3
    # conn = sqlite3.connect('ssq.db')
    conn = sqlite3.connect('{}.db'.format(db))
    c = conn.cursor()
    # 如果表test不存在 则创建test
    # c.execute("CREATE TABLE IF NOT EXISTS test(id INTEGER PRIMARY KEY,name TEXT,age INTEGER)")
    # c.execute("CREATE TABLE IF NOT EXISTS ssq(开奖日期 TEXT,期号 TEXT,号码 TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS {}({} TEXT,{} TEXT,{} TEXT)".format(table, row1, row2, row3))
    conn.commit()  # 一次性提交事务
    print("Records created successfully")
    conn.close()


def 是否最后一页(res, i):
    # 共2017条记录 1/101页      # &nbsp; ;<a disab
    pageMax = 文本_取中间文本(res, "共", "<")
    pageMax = 文本_取中间文本(pageMax, "/", "页")
    pageMax = int(pageMax)
    if i >= pageMax:
        return True
    else:
        return False


def main():
    # 解析第一页
    # @如果都在数据库 就不解析了
    # @如果部分已存在 部分新添加 也不继续解析
    # @如果 全部都需要添加入数据库  就需要继续解析

    # 解析数据 #添加进数据库

    # 如果到了最后一页 也不继续get_url了

    i = 1
    while True:
        # url = "https://www.lottery.gov.cn/historykj/history_1.jspx?_ltype=dlt"  # 首页 也可以是这种
        url = "https://www.lottery.gov.cn/historykj/history_{}.jspx?_ltype=dlt".format(i)  # 首页 也可以是这种
        res = get_首页(url)
        # time.sleep(2.5)  加到了子程序里面
        lis = 解析_首页(res)
        是否需要继续下载 = 对比_sqlite数据库(lis)  # 如果当前页面都是新的需要加入的数据 就需要继续get
        if 是否需要继续下载 == True:
            print("需要继续下载", "当前页", i)
        else:
            print("不需要继续下载", "当前页", i)
            break

        # ■最后一页就不在下载了    # ■注意 i 超过 pageMax
        if 是否最后一页(res, i):
            print("是最后一页", "不需要继续下载了", "当前页", i)
            break

        i = i + 1  # 继续下载 修改i


if __name__ == '__main__':
    t = time.time()

    # creat_sqlite()  # 数据库不存在 则创建数据库 创建表
    creat_sqlite("dlt", "dlt", "开奖日期", "期号", "号码")

    main()  # 主程序

    print("耗时", time.time() - t)

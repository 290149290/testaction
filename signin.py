
#  @完成爬虫 爬取一个网页 取简单结果 保存到指定txt中  原因:爬虫  包括创建文件夹

import time
import os


def save(file, res):
    with open(file, 'w', encoding='utf-8') as f:
        f.write(res)


def 文件_读入文本(file):
    try:
        with open(file, mode="r", encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # print('检测到编码可能是gbk,正在调用gbk...请稍候...')
        with open(file, mode="r", encoding='gbk') as f:
            return f.read()


def start_():
    print(time.ctime(), "要写文件了,不知道能否成功")
    save("hello.txt", "nowtime:" + time.ctime())
    print(time.ctime(), "这里是写完了")
    print(os.path.isfile("hello.txt"))
    print(文件_读入文本("hello.txt"))

def start():
    # 文件夹如果存在 exist_ok为True不会引发异常
    # os.makedirs("./txt文件夹",exist_ok=True) # --> 错了?
    file = "txt文件夹"
    os.makedirs(file,exist_ok=True)  # 文件夹如果存在 exist_ok为True不会引发异常
    # 测试linux虚拟环境下 新建文件夹
    save("./txt文件夹/hello.txt", "nowtime:" + time.ctime())

    os.makedirs("./txt文件夹1", exist_ok=True)  # --> 错了?
    save("./txt文件夹1/hello1.txt", "nowtime:" + time.ctime())


if __name__ == '__main__':
    start()

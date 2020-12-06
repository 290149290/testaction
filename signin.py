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


def start():
    print(time.ctime(), "要写文件了,不知道能否成功")
    save("hello.txt", "nowtime:" + time.ctime())
    print(time.ctime(), "这里是写完了")
    print(os.path.isfile("hello.txt"))
    print(文件_读入文本("hello.txt"))


if __name__ == '__main__':
    start()

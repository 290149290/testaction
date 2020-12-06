import time
import os

def save(file, res):
    with open(file, 'w', encoding='utf-8') as f:
        f.write(res)


def start():
    print(time.ctime(),"要写文件了,不知道能否成功")
    save("hello.txt", "world" + time.ctime())
    print(time.ctime(),"这里是写完了")
    print(os.path.isfile("hello.txt"))


if __name__ == '__main__':
    start()

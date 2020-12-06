import time


def save(file, res):
    with open(file, 'w', encoding='utf-8') as f:
        f.write(res)


def start():
    save("hello.txt", "world" + time.ctime())
    print(time.ctime())


if __name__ == '__main__':
    start()

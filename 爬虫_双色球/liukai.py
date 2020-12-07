
def 文件_是否存在(file, 只判断文件=True):
    # import pathlib
    # return pathlib.Path(file).is_file()
    # 方法1:
    # import pathlib
    # print(pathlib.Path(file).exists())  # 无论是文件还是文件夹 存在 就存在
    # print(pathlib.Path(file).is_file())  # 如果没有这个文件,哪怕是同名文件夹 也不行
    # 方法2:
    # import os
    # print(os.path.exists(file))  # 无论是文件还是文件夹 存在 就存在
    # print(os.path.isfile(file))  # 如果没有这个文件,哪怕是同名文件夹 也不行
    import os
    if 只判断文件:
        return os.path.isfile(file)  # 只判断文件
    else:
        return os.path.exists(file)  # 该路径只要存在,无论是文件还是文件夹,都可以
# 文本_读入文本   #一.文件不存在   二.文件编码是gb2312? /文件编码是utf8?
def 文件_读入文本(file):
    try:
        with open(file, mode="r", encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # print('检测到编码可能是gbk,正在调用gbk...请稍候...')
        with open(file, mode="r", encoding='gbk') as f:
            return f.read()

#覆写 覆盖写入
def 文本_写到文件(file,text):
    # 检查文件多级目录是否存在,如果不存在则创建目录
    import os
    directory = os.path.dirname(file)  # dir与内置方法dir()重名 会导致内置方法无效
    if not os.path.exists(directory):
        os.makedirs(directory)

    #覆盖式写入
    with open(file, 'w', encoding='utf-8') as f:
        f.write(text)

# 正则  #文本_取中间文本   文本_取中间文本
def 文本_取中间文本(string, front, behind, 标识自动转义=False):
    # 返回值:None 或者 str1
    # 示例1:文本_取中间文本('0123450123445','23','5') -->> '4'
    # 示例1:文本_取中间_批量('0123450123445','236','5') -->>None
    import re
    # search 只查1次  #符合条件就停止
    # re.search(正则表达式,string,re.S)会返回一个对象,然后对该对象使用.group(i)方法  #备注:这里是因为正则有分组(.*?) 所以才是.group(1)
    # print(re.search(front + '(.*?)' + behind, string, re.S))
    # print(re.search(front + '(.*?)' + behind, string, re.S).group(0))
    # return re.search(front + '(.*?)' + behind, string, re.S).group(1)   #■★bug:当无匹配时,返回值None是没有group方法的

    # front和behind 里面如果有元字符 比如() 就需要处理 否则影响正则表达式 导致取出None
    if 标识自动转义:
        for i in ".*?()[]":
            front = re.sub('[%s]' % i, "\\" + i, front)
            behind = re.sub('[%s]' % i, "\\" + i, behind)

    r = re.search(front + '(.*?)' + behind, string, re.S)
    return r.group(1) if r else None  # 问题:这里是否要改成""? 因为很多时候 是str1+str2+..这种组合来的?
    # return r.group(1) if r else r   #因为当r为None时 return r 等同于None


# 文本_取中间_批量   #正则
def 文本_取中间_批量(string, front, behind):
# def 文本_取中间_批量(string, front, behind, 标识自动转义=False):
    # 返回值:[] 或者 [str1,str2,...]
    # 示例1:文本_取中间_批量('0123450123445','23','5') -->> ['4','44']
    # 示例1:文本_取中间_批量('0123450123445','236','5') -->>[]
    """
    >>> 文本_取中间_批量('0123450123445','23','5')
    ['4', '44']
    >>> 文本_取中间_批量('0123450123445','236','5')
    []
    """
    import re

    # front和behind 里面如果有元字符 比如() 就需要处理 否则影响正则表达式 导致取出None
    '''
    if 标识自动转义:
        for i in ".*?()[]":
            if i in front:         front = re.sub('[{}]'.format(i), "\\" + i, front)
            if i in behind:        behind = re.sub('[{}]'.format(i), "\\" + i, behind)
            # front = re.sub('[%s]' % i, "\\" + i, front)
            # behind = re.sub('[%s]' % i, "\\" + i, behind)
            # 原先问题:不去判断 正则直接替换的话 会报错 : FutureWarning: Possible nested set at position 1
    '''

    for i in ".*?()[]":   #TODO 可能还有问题 因为元字符 还包括 + - \ ^ { } 等等
        # front = front.replace(i, "\\" + i)
        # behind = behind.replace(i, "\\" + i)
        if i in front:          front = front.replace(i, "\\" + i)
        if i in behind:         behind = behind.replace(i, "\\" + i)
        #【知识点:】如果不判断是否存在 直接使用替换时, replace方式 都不会报错

    # re.S 表示“.”（不包含外侧双引号，下同）的作用扩展到整个字符串，包括“\n”
    return re.findall(front + '(.*?)' + behind, string, re.S)


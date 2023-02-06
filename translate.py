#! /usr/bin/python3

from urllib.request import Request, urlopen
import json
import hashlib
import random
import os
import urllib.parse
import string
import sys
import fcntl

API_HTTPS = "https://fanyi-api.baidu.com/api/trans/vip/translate"
# 自动检测语种
FROM = 'auto'
To = 'zh'

# 应用id和密钥
APPID = os.environ.get('SHELL_TRANSLATE_APPID', None)
KEY = os.environ.get('SHELL_TRANSLATE_KEY', None)


def get_pipes():
    """获取管道输入"""
    fcntl.fcntl(sys.stdin, fcntl.F_SETFL, os.O_NONBLOCK)
    try:
        return sys.stdin.read()
    except TypeError:
        return None


def com_sign(query: str):
    """
    对参数进行签名
    :param query: 请求翻译query
    :return:
    """
    salt = "".join(random.choices(string.ascii_lowercase, k=8))
    sign_str = APPID + query + salt + KEY
    sign_md5 = hashlib.md5(sign_str.encode('utf-8')).hexdigest().lower()
    return {'salt': salt, 'sign': sign_md5}


def translate(query: str, from_: str = FROM, to: str = To, appid: str = APPID):
    """
    请求翻译指定的文档数据
    :param appid:
    :param query: 请求翻译query
    :param from_: 翻译源语言
    :param to:翻译目标语言
    :return:
    """
    salt, sign = com_sign(query).values()
    form = {
        'q': query,
        'from': from_,
        'to': to,
        'appid': appid,
        'salt': salt,
        'sign': sign,
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded;'
    }
    request = Request(
        url=API_HTTPS,
        data=urllib.parse.urlencode(form).encode('utf8'),
        method='POST',
        headers=headers
    )

    dst = json.loads(urlopen(request).read())['trans_result'][0]['dst']
    return dst


def get_query():
    """获取预翻译的文本"""
    if len(sys.argv) == 1:
        input_argv = None
    elif len(sys.argv) == 2:
        input_argv = sys.argv[-1]
    else:
        sys.stderr.write(f"收到多个参数 {'  '.join(sys.argv[1:])}\n")
        sys.exit(1)
    input_pipes = get_pipes()
    if input_argv and input_pipes:
        sys.stderr.write(f"管道输入与传参输入只能存在一个\n")

    return input_pipes or input_argv


def run():
    query = get_query()
    if query:
        query_lis = query.split('\n')
        query_lis = filter(bool, query_lis)
        for q in query_lis:
            # 输出原文
            print(q)
            # 输出译文
            print('\033[92m' + translate(q) + '\033[0m')


if __name__ == '__main__':
    if APPID is None or KEY is None:
        sys.stderr.write("请在环境变量中设置 SHELL_TRANSLATE_APPID 和 SHELL_TRANSLATE_KEY\n"
                         "他们可以在https://fanyi-api.baidu.com/manage/developer找到\n"
                         "SHELL_TRANSLATE_APPID 对应 APPID;SHELL_TRANSLATE_KEY对应密钥\n"
                         "参考代码,将将它们追加到你的`~/.bashrc`文件\n"
                         '\texport SHELL_TRANSLATE_APPID="你的 APPID"\n'
                         '\texport SHELL_TRANSLATE_KEY="你的密钥"\n')
        sys.exit(-1)
    run()

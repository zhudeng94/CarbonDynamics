#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/22/22 10:41 AM
# @Author  : Zhu Deng
# @Site    : https://github.com/zhudeng94
# @File    : main.py
# @Software: PyCharm

from Amap import getAmapIndex
import datetime


def main():
    # 初始化高德和TomTom的类
    a = getAmapIndex.Amap()

    # 每天执行一次高德和TomTom的天级数据抓取
    print('[AMAP] Updating hourly traffic index from Gaode...')
    a.getAmapData('Hourly')
    print('[AMAP] Updating daily traffic index from Gaode...')
    a.getAmapData('Daily')


if __name__ == '__main__':
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/22/22 9:49 AM
# @Author  : Zhu Deng
# @Site    : https://github.com/zhudeng94
# @File    : getAmapIndex.py
# @Software: PyCharm

import pandas as pd
import os
from tqdm import tqdm
import toolkit


class Amap:
    def __init__(self):
        self.cityList = None
        self.dataPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data')
        self.pathToCityList = os.path.join(self.dataPath, 'amapCityList.csv')

    def getCityList(self):
        res = toolkit.get_from_url('https://report.amap.com/ajax/getCityInfo.do?')
        self.cityList = pd.DataFrame(res.json())
        self.cityList.to_csv(self.pathToCityList, index=False)

    def getAmapData(self, interval='Daily'):
        if os.path.exists(self.pathToCityList):
            self.cityList = pd.read_csv(self.pathToCityList)
        else:
            self.getCityList()

        dataType = {
            1: '拥堵延时指数',            # '拥堵延时指数-实际旅行时间与自由流(畅通)状态下旅行时间的比值',
            2: '高延时运行时间占比',       # '高延时运行时间占比(%)-拥堵延时指数大于1.5的累计时长占比',
            3: '拥堵路段里程比',          # '拥堵路段里程比(%)-道路网中各等级道路分别处于拥堵、严重拥堵的路段里程比例加权求和所得',
            4: '平均车速',               # '平均车速(km/h)-道路网中驾车行驶的平均速度',
            # 5: '道路运行速度偏差率(%)-道路网中平均速度标准差与平均速度的比值',
            # {41:"高速",42:"国道",43:"快速路",44:"主干路",45:"次干路"}
        }

        url = 'https://report.amap.com/ajax/city%s.do?cityCode=%s&dataType=%s'
        print('[NEW] Started to download %s data...' % interval.lower())
        filename = os.path.join(self.dataPath, 'amap%sIndex.csv' % interval)
        new_df = pd.DataFrame()
        for _, row in tqdm(self.cityList.iterrows()):
            for dt in dataType:
                res = toolkit.get_from_url(u=url % (interval, row['code'], dt), retry=True, retry_waiting=30)
                tmp = pd.DataFrame(res.json())
                tmp.columns = ['timestamp', 'value']
                tmp['type'], tmp['code'], tmp['city'] = dt, row['code'], row['name']
                new_df = pd.concat([new_df, tmp])

        if os.path.exists(filename):
            pd.concat([pd.read_csv(filename, low_memory=False), new_df])\
                .drop_duplicates()\
                .sort_values(by=['type', 'code', 'timestamp'])\
                .to_csv(filename, index=False)
        else:
            new_df.drop_duplicates().sort_values(by=['type', 'code', 'timestamp']).to_csv(filename, index=False)

        print('[DONE] Success!')

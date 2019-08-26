#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# @Time    : 2019/8/22 下午10:29
# @Author  : Chilson
# @Email   : qiushun_fang@126.com

import re
import requests
import pickle


class StationName:
    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js'
    station_map = {}

    def download_station_js(self):
        """下载车站字典js文件"""
        r = requests.get(self.url)
        if r.status_code == 200:
            return r.text

    def parse_station_map(self, content):
        """
        解析车站字典
        :param content: 车站字典原始js文件
        :return:
        """
        useful_str = re.findall(r"'@(.*?)'", content)[0]
        name_strs = useful_str.split('@')
        for name_str in name_strs:
            try:
                name_split = name_str.split('|')
                self.station_map[name_split[1]] = name_split[2]
            except IndexError as e:
                raise e

    def save_station(self):
        """保存车站字典"""
        with open('station.pk', 'wb') as f:
            pickle.dump(self.station_map, f)

    def run(self):
        """主函数"""
        content = self.download_station_js()
        self.parse_station_map(content)
        print(self.station_map)
        self.save_station()

    def __repr__(self):
        return f'<Station - { self.url }> 车站中英对照字典'


if __name__ == '__main__':
    print(StationName())

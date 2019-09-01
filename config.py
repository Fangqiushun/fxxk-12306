#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# @Time    : 2019/8/22 下午11:27
# @Author  : Chilson
# @Email   : qiushun_fang@126.com

import pickle
import os
from fake_useragent import UserAgent

ua = UserAgent()
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # 余票查询结果表头索引字典
    TICKET_INFOS_MAP = {
        '余票代码': 12,
        '车号': 2,
        '车次': 3,
        '始发站': 4,
        '终点站': 5,
        '出发站': 6,
        '到达站': 7,
        '出发时间': 8,
        '到达时间': 9,
        '历时': 10,
        '是否当日达': 18,
        '是否能买': 11,
        '出发日期': 13,
        '商务座/特等座': 32,
        '一等座': 31,
        '二等座': 30,
        '高级软卧': 21,
        '软卧/一等卧': 23,
        '动卧': 33,
        '硬卧/二等卧': 28,
        '硬座': 29,
        '无座': 26,
        '备注': 1,
        '密码串': 0
    }

    # 存储余票字典
    LEFT_TICKET_MAP = {
        'left_ticket': '余票代码',
        'train_no': '车号',
        'station_train_code': '车次',
        'from_station_telecode': '出发站',
        'to_station_telecode': '到达站',
        'secret_str': '密码串'
    }

    # 生成站点字典
    with open(os.path.join(basedir, 'station.pk'), 'rb') as f:
        STATION_MAP = pickle.load(f)
        REVERSE_STATION_MAP = {value: key for key,
                               value in STATION_MAP.items()}

    HEADERS = {
        'User-Agent': ua.random
    }

    IMAGE_ANSWER = {
        '1': '40,40',
        '2': '110,40',
        '3': '180,40',
        '4': '260,40',
        '5': '40,120',
        '6': '110,120',
        '7': '180,120',
        '8': '260,120'
    }


config = {
    'base': Config
}

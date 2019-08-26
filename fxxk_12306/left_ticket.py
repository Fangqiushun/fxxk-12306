#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# @Time    : 2019/8/21 下午11:11
# @Author  : Chilson
# @Email   : qiushun_fang@126.com

import requests
from prettytable import PrettyTable
import json
from config import config
from fxxk_12306.logger import Logger

logger = Logger('leftTicket').get_logger()


class LeftTicket:

    def __init__(self, train_date, from_station, to_station):
        self.purpose_codes = 'ADULT'
        self.base_url = 'https://kyfw.12306.cn/otn/leftTicket'
        self.train_date = train_date
        self.from_station = config['base'].STATION_MAP.get(from_station)
        self.to_station = config['base'].STATION_MAP.get(to_station)
        self.headers = config['base'].HEADERS
        self.verify_station()

    def verify_station(self):
        if self.from_station not in config['base'].STATION_MAP.values():
            logger.error('出发站不存在...')
        if self.to_station not in config['base'].STATION_MAP.values():
            logger.error('到达站不存在...')

    def search_left_ticket(self):
        """
        查询余票
        :param train_date: 日期
        :param from_station: 出发站
        :param to_station: 到达站
        :return: 余票列表
        """
        payload = {
            'leftTicketDTO.train_date': self.train_date,
            'leftTicketDTO.from_station': self.from_station,
            'leftTicketDTO.to_station': self.to_station,
            'purpose_codes': self.purpose_codes
        }
        r = requests.get(self.base_url + '/query', params=payload, headers=self.headers)
        if r.status_code == 200:
            try:
                result = r.json().get('data', dict()).get('result')
                return result
            except json.decoder.JSONDecodeError as e:
                logger.error('没有搜索到对应的数据!')
                return None

    def parse_left_ticket(self, ticket_infos):
        """
        解析余票信息
        :param ticket_infos: 余票信息
        :return: 余票字典列表 ([{}, {}, ...])
        """
        ticket_infos_list = []
        ticket_infos_map = config['base'].TICKET_INFOS_MAP
        if ticket_infos:
            for ticket in ticket_infos:
                tds = ticket.split('|')
                row = {key:tds[ticket_infos_map[key]] for key in ticket_infos_map}
                ticket_infos_list.append(row)
        return ticket_infos_list

    def show_ticket_infos(self, ticket_infos_list):
        """
        展示余票信息
        :param ticket_infos_list:
        :return:
        """
        t = PrettyTable(config['base'].TICKET_INFOS_MAP.keys())
        for ticket_info in ticket_infos_list:
            t.add_row(ticket_info.values())
        logger.info(t)

    def __repr__(self):
        return f'<LeftTicket - { self.base_url }> 搜索余票信息'


if __name__ == '__main__':
    fxxk = LeftTicket('2019-09-13', '广州', '北京')
    print(fxxk)
    ticket_infos = fxxk.search_left_ticket()
    ticket_infos_list = fxxk.parse_left_ticket(ticket_infos)
    fxxk.show_ticket_infos(ticket_infos_list)

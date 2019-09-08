#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# @Time    : 2019/8/21 下午11:11
# @Author  : Chilson
# @Email   : qiushun_fang@126.com

import datetime
import json
import requests
import urllib3
from prettytable import PrettyTable
from config import Config
from fxxk_12306.logger import Logger

logger = Logger('leftTicket').get_logger()
# 不展示不做验证请求接口的警告
urllib3.disable_warnings()


class LeftTicket:
    """查询余票.
    思路以及实现步骤：
        1、查询余票
        2、展示余票
        3、存储实际可买的余票
    参数：
        train_date 坐车日期
        from_station 出发站
        to_station 到达站
        session 会话窗口（可有可无）
    """

    def __init__(self, train_date, from_station, to_station, session=None):
        self.purpose_codes = 'ADULT'
        self.base_url = 'https://kyfw.12306.cn/otn/leftTicket'
        self.train_date = train_date
        self.from_station = Config.STATION_MAP.get(from_station)
        self.to_station = Config.STATION_MAP.get(to_station)
        self.ticket_infos_map = Config.TICKET_INFOS_MAP
        self.left_ticket_map = Config.LEFT_TICKET_MAP
        self.headers = Config.HEADERS
        self.verify_station()
        self.session = session if session is not None else requests.Session()

    def post(self, url, data=None):
        return self.session.post(url=url, data=data, headers=self.headers, verify=False)

    def get(self, url, params=None):
        return self.session.get(url=url, params=params, headers=self.headers, verify=False)

    def verify_station(self):
        if self.from_station not in Config.STATION_MAP.values():
            logger.error('出发站不存在...')
        if self.to_station not in Config.STATION_MAP.values():
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
        r = self.get(url=self.base_url + '/queryT', params=payload)
        if r.status_code == 200:
            try:
                result = r.json().get('data', dict()).get('result')
                return result
            except json.decoder.JSONDecodeError as e:
                logger.error('没有搜索到对应的数据!')
                return None
        else:
            logger.error(f'查询失败（状态码：{ r.status_code }）')

    def parse_left_ticket(self, ticket_infos):
        """
        解析余票信息
        :param ticket_infos: 余票信息
        :return: 余票字典列表 ([{}, {}, ...])
        """
        ticket_infos_list = []
        if ticket_infos:
            for ticket in ticket_infos:
                tds = ticket.split('|')
                row = {key: tds[self.ticket_infos_map[key]]
                       for key in self.ticket_infos_map}
                ticket_infos_list.append(row)
        return ticket_infos_list

    def show_ticket_infos(self, ticket_infos_list):
        """
        展示余票信息
        :param ticket_infos_list: 余票信息列表
        :return:
        """
        t = PrettyTable(Config.TICKET_INFOS_MAP.keys())
        for ticket_info in ticket_infos_list:
            t.add_row(ticket_info.values())
        logger.info(t)

    def get_left_ticket(self, ticket_infos):
        """
        获取实际余票（可以买）
        :param ticket_infos: 余票信息
        :return:
        """
        left_tickets_list = []
        for ticket in ticket_infos:
            tds = ticket.split('|')
            if tds[self.ticket_infos_map['是否能买']] == 'Y':
                left_row = {key: tds[self.ticket_infos_map[self.left_ticket_map[key]]]
                            for key in self.left_ticket_map}
                left_row['from_station'] = Config.REVERSE_STATION_MAP.get(
                    left_row['from_station_telecode'])
                left_row['to_station'] = Config.REVERSE_STATION_MAP.get(
                    left_row['to_station_telecode'])
                left_tickets_list.append(left_row)
        return left_tickets_list

    def run(self):
        """主函数"""
        ticket_infos = self.search_left_ticket()
        ticket_infos_list = self.parse_left_ticket(ticket_infos)
        self.show_ticket_infos(ticket_infos_list)
        left_tickets_list = self.get_left_ticket(ticket_infos)
        return left_tickets_list

    def __repr__(self):
        return f'<LeftTicket - { self.base_url }> 搜索余票信息'


if __name__ == '__main__':
    fxxk = LeftTicket('2019-09-14', '广州', '普宁')
    left_tickets_list = fxxk.run()
    print(left_tickets_list)

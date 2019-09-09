#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# @Time    : 2019/8/24 下午11:38
# @Author  : Chilson
# @Email   : qiushun_fang@126.com

import sys
from config import Config
from fxxk_12306.logger import Logger

logger = Logger('Main').get_logger()


def show_left_ticket(train_date, from_station, to_station):
    """展示余票

    :param train_date: 出发日期
    :param from_station: 出发站
    :param to_station: 到达站
    :return:
    """
    from fxxk_12306.left_ticket import LeftTicket
    fxxk = LeftTicket(train_date, from_station, to_station)
    ticket_infos = fxxk.search_left_ticket()
    ticket_infos_list = fxxk.parse_left_ticket(ticket_infos)
    fxxk.show_ticket_infos(ticket_infos_list)


def search_and_order(train_date, from_station, to_station,
                     session, min_time=None, max_time=None, max_use_time=None):
    """查询余票并下单

    :param train_date: 出发日期
    :param from_station: 出发站
    :param to_station: 到达站
    :param session: 会话窗口(登录以后的会话窗口)
    :param min_time: 最早出发时间
    :param max_time: 最晚出发时间
    :param max_use_time: 最长坐车时间
    :return:
    """
    from fxxk_12306.order import Order
    from fxxk_12306.left_ticket import LeftTicket
    fxxk = LeftTicket(train_date, from_station, to_station, session)
    left_tickets_list = fxxk.run()
    order = Order(left_tickets_list, session, min_time, max_time, max_use_time)
    if order.ticket is not None:
        return order.run()
    else:
        return False


def shell_help():
    logger.info('\n参数列表:'
                '\n\t--help/-h 命令帮助'
                '\n\t--download_stations 下载车站中英对照文件'
                '\n\t--show_stations 所有车站展示'
                '\n\t--show_station 查询某个车站(需带一个参数值,<车站中文名/车站英文简称>)'
                '\n\t--search_ticket 查询车票(需带三个参数值,<乘车日期> <出发站> <到达站>)'
                '\n\t--login 登录(需带两个参数值,<账号> <密码>)')


def shell_download_stations():
    from station_name import StationName
    station = StationName()
    station.run()


def shell_show_stations():
    logger.info(Config.STATION_MAP.keys())


def shell_show_station():
    while True:
        station = input('请输入相查询的车站(输入q退出):')
        if station == 'q':
            sys.exit(0)
        station_map = Config.STATION_MAP
        reverse_station_map = Config.REVERSE_STATION_MAP
        if station in station_map.keys():
            logger.info(f'\n车站名: {station}'
                        f'\n简称: {station_map[station]}')
        elif station in reverse_station_map.keys():
            logger.info(f'\n车站名: {reverse_station_map[station]}'
                        f'\n简称: {station}')
        else:
            logger.error('没有对应的车站，请检查输入是否有误！')


def shell_search_ticket():
    train_date = input('出发日期<yyyy-mm-dd>:')
    from_station = input('出发站<中文名>:')
    to_station = input('到达站<中文名>:')
    show_left_ticket(train_date, from_station, to_station)


def shell_login():
    from fxxk_12306.login import Login
    username = input('请输入帐号:')
    password = input('请输入密码:')
    login = Login(username, password)
    login.run()
    return login.session


def shell_order():
    session = shell_login()
    train_date = input('出发日期<yyyy-mm-dd>:')
    from_station = input('出发站<中文名>:')
    to_station = input('到达站<中文名>:')
    min_time = input('最早乘车时间:')
    max_time = input('最晚乘车时间:')
    max_use_time = input('最长坐车时间:')
    order_result = False
    while not order_result:
        order_result = search_and_order(
            train_date, from_station, to_station, session, min_time, max_time, max_use_time)
        if order_result:
            from fxxk_12306.send_email import send_successful_email
            send_successful_email()


shell_map = {
    '--help': shell_help,
    '--download_stations': shell_download_stations,
    '--show_stations': shell_show_stations,
    '--show_station': shell_show_station,
    '--search_ticket': shell_search_ticket,
    '--login': shell_login,
    '--order': shell_order
}

if __name__ == '__main__':
    if len(sys.argv) > 1:
        func = shell_map.get(sys.argv[1])
        if func is not None:
            func()
        else:
            shell_help()
    else:
        shell_help()

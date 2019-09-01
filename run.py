#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# @Time    : 2019/8/24 下午11:38
# @Author  : Chilson
# @Email   : qiushun_fang@126.com

from fxxk_12306.left_ticket import LeftTicket, logger
from fxxk_12306.login import Login
import sys

def show_left_ticket(train_date, from_station, to_station):
    """
    展示余票
    :param train_date:
    :param from_station:
    :param to_station:
    :return:
    """
    fxxk = LeftTicket(train_date, from_station, to_station)
    ticket_infos = fxxk.search_left_ticket()
    ticket_infos_list = fxxk.parse_left_ticket(ticket_infos)
    fxxk.show_ticket_infos(ticket_infos_list)

argv = sys.argv
# 获取帮助
if len(argv) == 1 or argv[1] in ('--help', '-h'):
    logger.info('\n参数列表:'
                '\n\t--help/-h 命令帮助'
                '\n\t--show_stations 所有车站展示'
                '\n\t--show_station 查询某个车站(需带一个参数值,<车站中文名/车站英文简称>)'
                '\n\t--search_ticket 查询车票(需带三个参数值,<乘车日期> <出发站> <到达站>)')
elif len(argv) > 1:
    # 查看车站
    if argv[1] == '--show_stations':
        from config import config
        logger.info(config['base'].STATION_MAP.keys())
    elif argv[1] == '--show_station':
        if len(argv) < 3:
            logger.error('请添加车站中文名或者英文代码')
        else:
            from config import config
            station_map = config['base'].STATION_MAP
            reverse_station_map = config['base'].REVERSE_STATION_MAP
            if argv[2] in station_map.keys():
                logger.info(f'\n车站名: { argv[2] }'
                            f'\n简称: { station_map[argv[2]] }')
            elif argv[2] in reverse_station_map.keys():
                logger.info(f'\n车站名: { reverse_station_map[argv[2]] }'
                            f'\n简称: { argv[2] }')
            else:
                logger.error('没有对应的车站，请检查输入是否有误！')

    # 查车票
    elif argv[1] == '--search_ticket':
        if len(argv) < 5:
            logger.error('\n至少需要输入三个参数: '
                         '\ntrain_date: 出发日期<yyyy-mm-dd>,'
                         '\nfrom_station: 出发站<中文名>,'
                         '\nto_station: 到达站<中文名>')
        else:
            show_left_ticket(argv[2], argv[3], argv[4])
    elif argv[1] == '--login':
        if len(argv) < 4:
            logger.error('请输入账号、密码')
        else:
            login = Login(argv[2], argv[3])
            login.run()
    else:
        logger.info('请添加参数 --help 查询参数说明')

#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# @Time    : 2019/8/24 下午11:38
# @Author  : Chilson
# @Email   : qiushun_fang@126.com

from fxxk_12306.left_ticket import LeftTicket, logger
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
                '\n\t--show_station 所有车站展示'
                '\n\t--search_ticket 查询车票(需带三个参数值,<train_date> <from_station> <to_station>)')
elif len(argv) > 1:
    # 查看车站
    if argv[1] == '--show_station':
        from config import config
        logger.info(config['base'].STATION_MAP.keys())
    # 查车票
    elif argv[1] == '--search_ticket':
        if len(argv) < 5:
            logger.error('\n至少需要输入三个参数: '
                         '\ntrain_date: 出发日期<yyyy-mm-dd>,'
                         '\nfrom_station: 出发站<中文名>,'
                         '\nto_station: 到达站<中文名>')
        else:
            show_left_ticket(argv[2], argv[3], argv[4])
    else:
        logger.info('请添加参数 --help 查询参数说明')

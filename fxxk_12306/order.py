#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# @Time : 2019/9/1 11:55
# @Author  : Chilson
# @Email   : qiushun_fang@126.com

import os
import urllib3
import requests
import datetime
from config import config
from fxxk_12306.logger import Logger

logger = Logger('leftTicket').get_logger()
# 不展示不做验证请求接口的警告
urllib3.disable_warnings()


# /otn/leftTicket/submitOrderRequest
# /otn/confirmPassenger/getPassengerDTOs
# /otn/confirmPassenger/checkOrderInfo
# /otn/confirmPassenger/getQueueCount
# /otn/confirmPassenger/confirmSingleForQueue
# GET /otn/confirmPassenger/queryOrderWaitTime


class Order:
    """自动化下单
    思路以及实现步骤：
        1、发起下单窗口
        2、获取个人信息
        3、填充个人信息
        4、下单
        5、查询订单状态
    参数：
        left_tickets_list 余票列表
        session 会话窗口（需要传入登录后的会话窗口）
    """

    def __init__(self, left_tickets_list, session=None):
        self.session = session if session is not None else requests.Session()
        self.left_tickets_list = left_tickets_list
        self.headers = config['base'].HEADERS
        self.base_url = 'https://kyfw.12306.cn/otn'

    def post(self, url, data=None):
        return self.session.post(url=url, data=data, headers=self.headers, verify=False)

    def get(self, url, params=None):
        return self.session.get(url=url, params=params, headers=self.headers, verify=False)

    def submit_order_request(self):
        """发起下单申请"""
        data = {
            'secretStr': self.left_tickets_list[0]['secret_str'],
            'train_date': datetime.datetime.strptime(self.left_tickets_list[0]['train_date'], '%Y%m%d').strftime('%Y-%m-%d'),
            'back_train_date': datetime.datetime.now().strftime('%Y-%m-%d'),
            'tour_flag': 'dc',
            'purpose_codes': 'ADULT',
            'query_from_station_name': self.left_tickets_list[0]['from_station'],
            'query_to_station_name': self.left_tickets_list[0]['to_station'],
            'undefined': ''
        }
        res = self.post(url=self.base_url +
                        '/leftTicket/submitOrderRequest', data=data)
        return res

    def run(self):
        res = self.submit_order_request()
        print(res.json())


if __name__ == '__main__':
    from fxxk_12306.left_ticket import LeftTicket
    from fxxk_12306.login import Login
    fxxk = LeftTicket('2019-09-14', '广州', '普宁')
    left_tickets_list = fxxk.run()
    login = Login(os.environ.get('USERNAME'), os.environ.get('PASSWORD'))
    login.run()
    order = Order(left_tickets_list, login.session)

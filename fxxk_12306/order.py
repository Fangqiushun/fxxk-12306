#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# @Time : 2019/9/1 11:55
# @Author  : Chilson
# @Email   : qiushun_fang@126.com

import os
import sys
import re
import urllib3
import requests
import datetime
import json
from urllib.parse import unquote
from config import Config
from fxxk_12306.logger import Logger

logger = Logger('leftTicket').get_logger()
# 不展示不做验证请求接口的警告
urllib3.disable_warnings()


class Order:
    """自动化下单
    思路以及实现步骤：
        1、根据策略选票
        2、发起下单请求
        3、获取下单需要的token跟key值
        4、获取乘车人信息
        5、请求验证码
        6、检查订单信息
        7、下单
    参数：
        left_tickets_list 余票列表
        session 会话窗口（需要传入登录后的会话窗口）
    """

    def __init__(self, left_tickets_list, session=None):
        self.session = session if session is not None else requests.Session()
        self.left_tickets_list = left_tickets_list
        self.headers = Config.HEADERS
        self.base_url = 'https://kyfw.12306.cn/otn'
        self.ticket = {}

    def select_ticket(self):
        """根据策略选票"""
        self.ticket = self.left_tickets_list[0]

    def post(self, url, data=None):
        return self.session.post(url=url, data=data, headers=self.headers, verify=False)

    def get(self, url, params=None):
        return self.session.get(url=url, params=params, headers=self.headers, verify=False)

    def submit_order_request(self):
        """发起下单申请"""
        data = {
            'secretStr': unquote(self.ticket['secret_str']),
            'train_date': datetime.datetime.strptime(self.ticket['train_date'], '%Y%m%d').strftime('%Y-%m-%d'),
            'back_train_date': datetime.datetime.now().strftime('%Y-%m-%d'),
            'tour_flag': 'dc',
            'purpose_codes': 'ADULT',
            'query_from_station_name': self.ticket['from_station'],
            'query_to_station_name': self.ticket['to_station'],
            'undefined': ''
        }
        res = self.post(url=self.base_url +
                        '/leftTicket/submitOrderRequest', data=data)
        return res

    def get_repeat_submit_token_key(self, res):
        """获取下单时需要的token、key

        :param res: 发起下单申请的结果（用于判断当前是否可以下单）
        :return: {'repeat_submit_token': '***', 'key_check_is_change': '***'}
        """
        try:
            res_json = res.json()
            if res_json['httpstatus'] == 200 and res_json['status'] == True:
                data = {'_json_att': ''}
                response = self.post(
                    url=self.base_url + '/confirmPassenger/initDc', data=data).text
                pattern = re.compile(
                    "globalRepeatSubmitToken = '(.*?)'.*?'key_check_isChange':'(.*?)'", re.DOTALL)
                result = pattern.findall(response)
                repeat_submit_token = result[0][0] if len(result) else ''
                key_check_is_change = result[0][1] if len(
                    result) and len(result[0]) > 1 else ''
                return {
                    'repeat_submit_token': repeat_submit_token,
                    'key_check_is_change': key_check_is_change
                }
            else:
                logger.error(','.join(res_json.get(
                    'messages', ['无法获取下单token，原因不明'])))
                sys.exit(0)
        except json.JSONDecodeError as e:
            logger.error('提交申请下单请求失败！')
            sys.exit(0)

    def get_passenger_info(self, repeat_submit_token):
        """获取乘车人信息"""
        get_passenger_url = self.base_url + '/confirmPassenger/getPassengerDTOs '
        data = {
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': repeat_submit_token
        }
        res = self.post(url=get_passenger_url, data=data)
        try:
            passenger = res.json()
            normal_passengers = passenger['data']['normal_passengers'][0]
            return normal_passengers
        except:
            logger.error('获取乘车人信息失败！')
            sys.exit(0)

    def generate_passenger_ticket(self, passenger):
        """生成乘车人信息拼接字符串"""
        passenger_ticket = 'O,0,1,{passenger_name},{passenger_type},{passenger_id_no},{mobile_no},N,{all_enc_str}'\
            .format(passenger_name=passenger['passenger_name'],
                    passenger_type=passenger['passenger_type'],
                    passenger_id_no=passenger['passenger_id_no'],
                    mobile_no=passenger['mobile_no'],
                    all_enc_str=passenger['allEncStr'])
        return passenger_ticket

    def generate_old_passenger(self, passenger):
        """生成旧乘车人信息拼接字符串"""
        old_passenger = '{passenger_name},{passenger_type},{passenger_id_no},1_'.format(
            passenger_name=passenger['passenger_name'],
            passenger_type=passenger['passenger_type'],
            passenger_id_no=passenger['passenger_id_no'])
        return old_passenger

    def get_pass_code(self):
        """获取验证码
        现在不确定是否有用，没有用到返回的数据，但是不是发送请求后有执行更新后端的数据不清楚
        """
        get_pass_code_url = self.base_url + '/passcodeNew/getPassCodeNew'
        params = {
            'module': 'passenger',
            'rand': 'randp'
        }
        get_pass_code_res = self.get(url=get_pass_code_url, params=params)

    def check_order_info(self, passenger, repeat_submit_token):
        """检查订单信息，确认无误才可以下单

        :param passenger: 乘车人信息
        :param repeat_submit_token: token
        :return: bool值，True信息正确
        """
        data = {
            'cancel_flag': '2',
            'bed_level_order_num': '000000000000000000000000000000',
            'passengerTicketStr': self.generate_passenger_ticket(passenger),
            'oldPassengerStr': self.generate_old_passenger(passenger),
            'tour_flag': 'dc',
            'randCode': '',
            'whatsSelect': 1,
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': repeat_submit_token
        }
        check_order_info_url = self.base_url + '/confirmPassenger/checkOrderInfo'
        check_order_info_res = self.post(url=check_order_info_url, data=data)
        res_json = check_order_info_res.json()
        if res_json['httpstatus'] == 200 \
            and res_json['status'] == True \
            and res_json['data'].get('submitStatus') == True:
            return True
        else:
            return False

    def confirm_single_for_queue(self, passenger, repeat_submit_token, key_check_is_change):
        """下单

        :param passenger: 乘车人信息
        :param repeat_submit_token: token
        :param key_check_is_change: key
        :return: bool值，True代表下单成功
        """
        data = {
            'passengerTicketStr': self.generate_passenger_ticket(passenger),
            'oldPassengerStr': self.generate_old_passenger(passenger),
            'randCode': '',
            'purpose_codes': '00',
            'key_check_isChange': key_check_is_change,
            'leftTicketStr': self.ticket['left_ticket'],
            'train_location': self.ticket['train_location'],
            'choose_seats': '',
            'seatDetailType': '000',
            'whatsSelect': '1',
            'roomType': '00',
            'dwAll': 'N',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': repeat_submit_token
        }
        confirm_single_for_queue_url = self.base_url + \
            '/confirmPassenger/confirmSingleForQueue'

        confirm_single_for_queue_res = self.post(url=confirm_single_for_queue_url, data=data)
        res_json = confirm_single_for_queue_res.json()
        if res_json['httpstatus'] == 200 \
            and res_json['status'] == True \
            and res_json['data'].get('submitStatus') == True:
            return True
        else:
            return False

    def run(self):
        self.select_ticket()
        res = self.submit_order_request()
        token_key = self.get_repeat_submit_token_key(res)
        repeat_submit_token = token_key['repeat_submit_token']
        key_check_is_change = token_key['key_check_is_change']
        passenger = self.get_passenger_info(repeat_submit_token)
        if self.check_order_info(passenger, repeat_submit_token):
            logger.info('检查订单信息成功了，下一步就下单了哦。。。')
            # order = self.confirm_single_for_queue(passenger, repeat_submit_token, key_check_is_change)
            # if order:
            #     logger.info('恭喜你，下单成功了，请在30分钟内点击后面的链接支付哦！\n')
            # else:
            #     logger.error('很遗憾，下单失败了，请确认是否重新下单（Y/N，默认3秒后重新下单。）？')
        else:
            logger.error('检查订单信息错误，请确认是否重新下单（Y/N，默认3秒后重新下单。）？')


if __name__ == '__main__':
    from fxxk_12306.left_ticket import LeftTicket
    from fxxk_12306.login import Login
    fxxk = LeftTicket('2019-09-14', '广州', '普宁')
    left_tickets_list = fxxk.run()
    login = Login(os.environ.get('USERNAME'), os.environ.get('PASSWORD'))
    login.run()
    order = Order(left_tickets_list, login.session)
    order.run()

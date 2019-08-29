#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# @Time    : 2019/8/26 下午9:33
# @Author  : Chilson
# @Email   : qiushun_fang@126.com
import requests
from PIL import Image
from prettytable import PrettyTable
import base64
from selenium import webdriver
import time
from config import config
from fxxk_12306.logger import Logger

logger = Logger('Login').get_logger()


class Login:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.base_url = 'https://kyfw.12306.cn'
        self.headers = config['base'].HEADERS
        self.session = requests.Session()
        self.img_path = 'image.jpg'
        self.image_answer = config['base'].IMAGE_ANSWER

    def save_image64(self):
        """保存验证图片"""
        img_url = self.base_url + \
            '/passport/captcha/captcha-image64?login_site=E&module=login&rand=sjrand'
        res = self.session.get(url=img_url, headers=self.headers).json()
        img = base64.b64decode(res.get('image'))

        with open(self.img_path, 'wb') as f:
            f.write(img)

    def translate_image_answer(self, input_code_list):
        """输入编号转换"""
        try:
            return ','.join([self.image_answer[i] for i in input_code_list])
        except KeyError as e:
            logger.error('输入错误,请重新输入!')
            self.check_image()

    def show_image_location(self):
        """展示图片对应数字位置"""
        table = PrettyTable()
        table.add_row([1, 2, 3, 4])
        table.add_row([5, 6, 7, 8])
        print(table)

    def show_image(self):
        Image.open(self.img_path).show()

    def check_image(self):
        """验证图片"""
        self.show_image()
        self.show_image_location()
        input_code = input("请在1—8中选择输入验证图片编号, 以','隔开.\n")
        input_code_list = input_code.split(',')
        answer = self.translate_image_answer(input_code_list)
        data = {
            'answer': answer,
            'login_site': 'E',
            'rand': 'sjrand'
        }
        check_url = self.base_url + '/passport/captcha/captcha-check'
        check_result = self.session.get(
            url=check_url, params=data, headers=self.headers).json()
        if check_result['result_code'] == '4':
            logger.info('*' * 10 + '图片验证通过!!!' + '*' * 10)
        else:
            logger.warning(' ^@._.@^ ' + '验证错误,请睁大你的眼睛看清楚...' + ' ^@._.@^ ')
            self.recheck_image()
        return answer

    def recheck_image(self):
        """重新检查验证图"""
        self.save_image64()
        self.check_image()

    def update_cookies(self):
        """更新cookie,否则登录不了"""
        driver = webdriver.PhantomJS()
        driver.get(self.base_url)
        # 等待1秒，留时间给浏览器跑js脚本，设置cookie
        time.sleep(1)
        cookies = driver.get_cookies()
        for cookie in cookies:
            if cookie['name'] == 'RAIL_DEVICEID':
                self.session.cookies.set('RAIL_DEVICEID', cookie['value'])
        if self.session.cookies.get('RAIL_DEVICEID') is None:
            logger.error('更新cookies失败!')

    def login(self, answer):
        """
        登录
        :param answer: 验证图片答案
        :return:
        """
        login_url = self.base_url + '/passport/web/login'
        data = {
            'username': self.username,
            'password': self.password,
            'appid': 'otn',
            'answer': answer
        }
        print(self.session.cookies)
        login_result = self.session.post(
            url=login_url, data=data, headers=self.headers)
        if login_result.status_code != 200:
            logger.error(f'({ login_result.status_code })登录失败了...')
        print(login_result.text)

    def get_session(self):
        """获取会话窗口"""
        return self.session

    def run(self):
        """主函数"""
        self.save_image64()
        answer = self.check_image()
        self.update_cookies()
        self.login(answer)

    def __repr__(self):
        return f'<Login - { self.base_url }> 模拟登录'


if __name__ == '__main__':
    login = Login('', '')
    login.run()

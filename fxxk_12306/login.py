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
import json
from config import config
from fxxk_12306.logger import Logger

logger = Logger('Login').get_logger()


class Login:
    """模拟登录12306.
    思路以及实现步骤：
        1、通过验证码
        2、更新cookies
        3、账号密码登录
        4、获取app的token
        5、验证token
    参数：
        username 账号名（一般为手机号码）
        password 账号密码
    """

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.base_url = 'https://kyfw.12306.cn'
        self.headers = config['base'].HEADERS
        self.session = requests.Session()
        self.img_path = 'image.jpg'
        self.image_answer = config['base'].IMAGE_ANSWER

    def post(self, url, data=None):
        return self.session.post(url=url, data=data, headers=self.headers, verify=False)

    def get(self, url, data=None):
        return self.session.get(url=url, data=data, headers=self.headers, verify=False)

    def save_image64(self):
        """保存验证图片"""
        img_url = self.base_url + \
            '/passport/captcha/captcha-image64?login_site=E&module=login&rand=sjrand'
        res = self.post(url=img_url).json()
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
        """
        验证图片
        :return: 图片答案对应的像素位置
        """
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
        check_result = self.get(url=check_url, data=data).json()
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
        driver.get('https://www.12306.cn')
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
        login_result = self.post(url=login_url, data=data)

        if login_result.status_code != 200:
            logger.error(f'很遗憾，登录失败了({login_result.status_code})...')
        try:
            res_json = login_result.json()
            if res_json.get('result_message') == '登录成功':
                self.session.cookies.set('uamtk', res_json.get('uamtk'))
                logger.info('*' * 10 + '恭喜你，登录成功啦！' + '*' * 10)
        except json.decoder.JSONDecodeError as e:
            logger.error(
                f'登录接口没有返回json文件，检查cookies设置是否正确：{ self.session.cookies }')

    def get_app_tk(self):
        """获取app的token"""
        data = {'appid': 'otn'}
        res = self.post(self.base_url + '/passport/web/auth/uamtk', data=data)
        if res.status_code == 200:
            res_json = res.json()
            if res_json.get('result_code') == 0:
                app_tk = res_json.get('newapptk')
                return app_tk

    def auth_client(self, app_tk):
        """
        客户端验证token是否有效
        :param app_tk:
        :return:
        """
        data = {'tk': app_tk}
        res = self.post(self.base_url + '/otn/uamauthclient', data=data)
        if res.status_code == 200:
            res_json = res.json()
            if res_json.get('result_code') == 0:
                logger.info('*' * 10 + '恭喜你，客户端认证成功啦！' + '*' * 10)
                return True
        return False

    def get_session(self):
        """获取会话窗口"""
        return self.session

    def run(self):
        """主函数"""
        self.save_image64()
        answer = self.check_image()
        self.update_cookies()
        self.login(answer)
        app_tk = self.get_app_tk()
        self.auth_client(app_tk)

    def __repr__(self):
        return f'<Login - { self.base_url }> 模拟登录'


if __name__ == '__main__':
    login = Login('', '')
    login.run()

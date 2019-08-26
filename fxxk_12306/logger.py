#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# @Time    : 2019/8/25 上午12:18
# @Author  : Chilson
# @Email   : qiushun_fang@126.com

import logging

class Logger:

    def __init__(self, name):
        self.logger = logging.Logger(name)

        # 定义控制台logger输出格式
        sh = logging.StreamHandler()
        formatter = logging.Formatter(
            '[%(asctime)s] %(filename)s->%(funcName)s line:%(lineno)d [%(levelname)s]%(message)s')
        sh.setFormatter(formatter)
        sh.setLevel(logging.INFO)

        self.logger.addHandler(sh)

    def get_logger(self):
        return self.logger
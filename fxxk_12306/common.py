#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# @Time    : 2019/9/9 下午10:52
# @Author  : Chilson
# @Email   : qiushun_fang@126.com

from config import Config

headers = Config.HEADERS


def post(session, url, data=None):
    return session.post(url=url, data=data, headers=headers, verify=False)


def get(session, url, params=None):
    return session.get(url=url, params=params, headers=headers, verify=False)

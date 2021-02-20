#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Descripttion:
version:
Author: zhangwei
Date: 2021-01-07 09:00:00
LastEditors: Please set LastEditors
LastEditTime: 2021-01-07 09:00:00
'''

import os.path


class User:

    # 初始化方法
    def __init__(self):
        self.userfile = os.getcwd() + '/source/users'
        self.users = []

        if not os.path.isfile(self.userfile):
            print(self.userfile)
            exit('账户文件不存在')

    def getUsers(self):
        with open(self.userfile) as f:
            self.users = [user.rstrip("\n") for user in f.readlines()]
        return self.users

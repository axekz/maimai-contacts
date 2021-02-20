#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Descripttion:
version:
Author: zhangwei
Date: 2021-01-07 09:00:00
LastEditors: Please set LastEditors
LastEditTime: 2021-01-07 09:00:00
'''

import os


class Log:
    def __init__(self, file, path='log'):
        self.path = os.getcwd() + '/' + path + '/'
        self.file = self.path + file
        self.fd = open(self.file, "a+")

    def log(self, content):
        self.fd.write(str(content) + '\n')

    def check(self):
        return os.path.isfile(self.file)

    def get(self):
        with open(self.file) as f:
            v = f.read()
        return v

    def __del__(self):
        self.fd.close()

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

import os, sys
import traceback
import time
import threading
import random

sys.path.append(os.getcwd() + '/src/')
from log import Log
from login import Login
from contact import Contact


class MyThread(threading.Thread):
    def __init__(self, threadID, name, data):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.data = data

        self.code = 0
        self.exception = ''
        self.exc_traceback = ''

    def run(self):
        try:
            self._run()
        except Exception as e:
            self.code = 1
            self.exception = e
            self.exc_traceback = ''.join(traceback.format_exception(*sys.exc_info()))

    def _run(self):
        print(self.name + ' starting ..')

        randNum = random.randint(1, 20)
        print('sleep ' + str(randNum))
        time.sleep(randNum)

        login = Login(self.data)
        cookie = login.getCookies()

        setattr(self.data, 'cookie', cookie)

        contact = Contact(self.data)
        contact.run()

        print(self.name + ' ending ..')

#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Descripttion: 
version: 
Author: zhangwei
Date: 2020-09-07 22:59:57
LastEditors: Please set LastEditors
LastEditTime: 2020-12-10 11:18:52
'''

import sys
import getopt
import time
from src.user import User
from src.word import Word
from src.data import Data
from src.thread import MyThread
from src.log import Log


class Maimai:
    def __init__(self):
        self.type = 2  # 抓取类型：1 全部，2 第一页
        self.pause = 20  # 每天晚上停止的时间
        self.rollStart = 50  # 翻页抓取间隔时间随机数起始时间 （与rollEnd配合使用）
        self.rollEnd = 180  # 翻页抓取间隔时间随机数终止时间 （与rollEnd配合使用）
        self.isOpenBrowser = False  # 是否打开浏览器窗口
        self.autoCloseBrowser = True  # 是否自动关闭浏览器窗口
        self.users = ''
        self.words = ''
        self.threads = []

    def main(self):
        print('main start ..')

        self.getUsers()
        self.getWords()

        self.createThreads()
        self.runThreads()

        print('main end ..')

    def getUsers(self):
        user = User()
        self.users = user.getUsers()
        return

    def getWords(self):
        word = Word()
        self.words = word.getWords()
        return

    def createThreads(self):
        for u in self.users:
            i = self.users.index(u)
            w = self.words[i]

            if not w:
                print('index ' + str(i) + ' not found word')
                continue

            user = u.split(',')
            threadId = int(i) + 1
            threadName = 'thread-' + user[0]

            data = Data(self.getIsTest())
            setattr(data, 'username', user[0])
            setattr(data, 'passwd', user[1])
            setattr(data, 'isOpenBrowser', self.isOpenBrowser)
            setattr(data, 'autoCloseBrowser', self.autoCloseBrowser)
            setattr(data, 'word', w)
            setattr(data, 'type', self.type)
            setattr(data, 'pause', self.pause)
            setattr(data, 'log', '-'.join([user[0], time.strftime('%Y%m%d'), w]))

            self.threads.insert(i, MyThread(threadId, threadName, data))
        return

    def runThreads(self):
        for t in self.threads:
            t.start()
        for t in self.threads:
            t.setDaemon(True)
            t.join()
        for t in self.threads:
            if t.code == 1:
                excep = Log(t.getName(), 'exception')
                excep.log('----------')
                excep.log(t.exc_traceback)
        return

    def getIsTest(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], "-o", ["online"])
        except getopt.GetoptError as err:
            print(str(err))
            exit()
        isTest = True
        for o, v in opts:
            if o in ("-o", "--online"):
                isTest = False
        return isTest


maimai = Maimai()
maimai.main()

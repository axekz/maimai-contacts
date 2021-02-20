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

import os, sys
import requests
import time, datetime
import random

sys.path.append(os.getcwd() + '/src/')
from log import Log


class Contact:

    # 初始化方法
    def __init__(self, data):
        self.cookieStr = data.cookie
        self.word = data.word
        self.type = data.type
        self.pause = data.pause
        self.api = data.api
        self.jsonContent = {}
        self.pageIndex = 0
        self.pageCount = 20
        self.proxy = data.proxy
        self.log = Log(data.log, 'log')
        self.data = Log(data.log, 'data')
        self.storage = Log(data.log, 'storage')

        self.pageIndex = self.storage.get() if self.storage.check() else 0

    def getContacts(self, word, pageIndex, isLoop=False):
        self.pageIndex = pageIndex
        self.checkTime()

        contactsInfoURL = "https://maimai.cn/search/contacts?count={}&page={}&query={}&dist=0&searchTokens=&highlight=true&jsononly=1&pc=1"

        url = contactsInfoURL.format(self.pageCount, pageIndex, word)
        headers = {'cookie': self.cookieStr}

        if not self.proxy:
            req = requests.get(url=url, headers=headers, verify=False, proxies=self.proxy)  # 最基本的GET请求
        else:
            req = requests.get(url=url, headers=headers, verify=False)  # 最基本的GET请求

        self.log.log('--原始数据--')
        self.log.log(req.text)
        self.jsonContent = req.json()

        if isLoop:
            return

        if "Invalid login user" in self.jsonContent:
            self.log.log('登录失效，请重置userCookie.txt文件')
            exit()

        if "data" not in self.jsonContent:
            self.log.log('数据不存在')
            self.log.log(self.jsonContent)
            if "result" in self.jsonContent:
                self.log.log('可能已封禁，需要验证')
            return

        if self.type == 2:
            self.saveContacts()
            self.end()
            self.log.log('抓取完成了')
            return

        if self.jsonContent['data']['contacts_total'] == 0:
            self.log.log('抓取完成了')
            return

        contactsTotal = self.jsonContent['data']['contacts_total']
        total = int(contactsTotal / self.pageCount) \
            if (contactsTotal % self.pageCount) == 0 \
            else int(contactsTotal / self.pageCount) + 1
        for index in range(total):
            if index > 0:
                self.log.log(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                self.log.log('抓取第{}页数据'.format(index))
                self.getContacts(word, index, True)
                self.saveContacts()
                time.sleep(random.randint(50, 180))

        self.end()
        self.log.log('抓取完成了')
        return

    def saveContacts(self):
        for v in self.jsonContent['data']['contacts']:
            contact = v['contact']
            list = [contact['career'],
                    contact['city'],
                    contact['company'],
                    contact['line4'],
                    contact['loc'],
                    contact['mem_point'],
                    contact['name'],
                    contact['position'],
                    str(contact['gender']),
                    contact['user_pfmj']['mj_name1'],
                    contact['user_pfmj']['pf_name1']]
            people = '--'.join(item for item in list)
            self.log.log(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            self.data.log(people)
            contact['search_by_word'] = self.word
            self.postData(contact)

    def postData(self, json):
        try:
            r = requests.post(self.api, json=json).json()
            self.log.log('--api return--')
            self.log.log(r.text)
        except Exception as e:
            self.log.log('--api exception--')
            self.log.log(e)
        return

    def checkTime(self):
        hour = int(time.strftime('%H'))
        if hour >= self.pause:
            self.pause()

    def pause(self):
        self.storage.log(str(self.pageIndex))
        self.log.log('')
        self.log.log('pause ..')
        exit()

    def end(self):
        self.log.log('')
        self.log.log('end ..')
        exit()

    def run(self):
        self.getContacts(self.word, self.pageIndex)

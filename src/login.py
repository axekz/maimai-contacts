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

import time
import os.path
import json
from selenium import webdriver


class Login:

    # 初始化方法
    def __init__(self, data):
        self.chromeDriverPath = os.getcwd() + "/src/chromedriver"
        self.loginWaitSecond = 3  # 输入完用户密码等待登录的时间
        # 登录的URL
        self.loginUrl = "https://maimai.cn/web/feed_explore"
        self.username = data.username
        self.password = data.passwd
        self.isOpenBrowser = data.isOpenBrowser
        self.autoCloseBrowser = data.autoCloseBrowser

        filepath = os.getcwd() + '/cookie/' + time.strftime('%Y-%m-%d')
        if not os.path.exists(filepath):
            os.mkdir(filepath)

        self.cookieFile = filepath + '/' + self.username + '.cookie'
        self.cookies = ''
        self.cookieStr = ''

        if not self.checkCookies():
            # 创建chrome启动选项
            chrome_options = webdriver.ChromeOptions()
            if not self.isOpenBrowser:
                # 指定chrome启动类型为headless 并且禁用gpu
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--disable-gpu')
            self.driver = webdriver.Chrome(self.chromeDriverPath, options=chrome_options)

        self.run()

    # 登录获取cookie
    def login(self):
        self.driver.get(self.loginUrl)

        time.sleep(self.loginWaitSecond)

        self.inputUserName()
        self.inputPassword()
        self.submitLogin()

    def inputUserName(self):
        self.driver.find_element_by_class_name("loginPhoneInput").send_keys(self.username)

    def inputPassword(self):
        self.driver.find_element_by_id("login_pw").send_keys(self.password)

    def submitLogin(self):
        self.driver.find_element_by_class_name("loginBtn").click()

    def readCookies(self):
        self.cookies = self.driver.get_cookies()

    # cookie 写入本地，利于查看,且可返回cookies string
    def saveCookies(self):
        cookie = [item["name"] + "=" + item["value"] for item in self.cookies]
        self.cookiestr = ';'.join(item for item in cookie)
        f = open(self.cookieFile, "a+")
        f.write(self.cookiestr)
        f.close()

    def checkCookies(self):
        return os.path.isfile(self.cookieFile)

    def getCookies(self):
        cookie = ''
        with open(self.cookieFile) as f:
            cookie = f.read()
        return cookie

    def __del__(self):
        if hasattr(self, 'driver') and self.autoCloseBrowser:
            self.driver.close()

    def run(self):

        if self.checkCookies():
            print('cookie存在，不重新登录')
            pass
        else:
            self.login()
            self.readCookies()
            self.saveCookies()
            print('cookie:')
            print(self.cookiestr)

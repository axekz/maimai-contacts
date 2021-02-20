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


class Word:

    # 初始化方法
    def __init__(self):
        self.wordsFile = os.getcwd() + '/source/words'
        self.words = []

        if not os.path.isfile(self.wordsFile):
            exit('关键词文件不存在')

    def getWords(self):
        with open(self.wordsFile) as f:
            self.words = [kw.rstrip("\n") for kw in f.readlines()]
        print('words:')
        print(self.words)
        return self.words

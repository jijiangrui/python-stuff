#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2018/7/24 14:09
# @Author  : capton
# @FileName: util.py
# @Software: PyCharm
# @Blog    : http://ccapton.cn
# @Github  : https://github.com/ccapton
# @Email   : chenweibin1125@foxmail.com

import os

def checkfile(path):
    if not path:
        return False,-1
    if os.path.isfile(path):
        return True, 1
    elif os.path.isdir(path):
        return True, 0
    else:
        return False, -1


def judge_unit(size):
    if size / 1024 / 1024 / 1024 >= 1:
        show_size = size / 1024 / 1024 / 1024
        unit = 'Gb'
    elif size / 1024 / 1024 >= 1:
        show_size = size / 1024 / 1024
        unit = 'Mb'
    elif size / 1024 >= 1:
        show_size = size / 1024
        unit = 'Kb'
    else:
        show_size = size
        unit = 'b'
    return (show_size, unit)


def relative_path(root,absolute_path):
    relative_path = str(absolute_path)[str(absolute_path).find(root)+len(root)+1:]
    if not relative_path:
        relative_path = ''
    return relative_path

import platform
def dir_divider():
    if platform.platform().find('Windows') != -1:
        return '\\'
    else:
        return '/'

def anti_dir_divider():
    if platform.platform().find('Windows') != -1:
        return '/'
    else:
        return '\\'

if __name__ == '__main__':
      pass


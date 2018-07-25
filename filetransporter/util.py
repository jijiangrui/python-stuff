#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2018/7/24 14:09
# @Author  : capton
# @FileName: util.py
# @Software: PyCharm
# @Blog    : http://ccapton.cn
# @Github  : https://github.com/ccapton
# @Email   : chenweibin1125@foxmail.com


def checkfile(path):
    if not path:
        return False,-1
    import os
    if os.path.isfile(path):
        return True, 1
    elif os.path.isdir(path):
        return True, 0
    else:
        return False, -1

def formated_size(size):
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
    return '%.2f' % show_size + unit

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


def dir_divider():
    import platform
    if platform.platform().find('Windows') != -1:
        return '\\'
    else:
        return '/'

def anti_dir_divider():
    import platform
    if platform.platform().find('Windows') != -1:
        return '/'
    else:
        return '\\'

def print_author_info(program_name):
    print('*'*60)
    line = 9
    while line > 0:
      if line == 8:
          print('。  %s' % program_name)
      elif line == 6:
          print('。  @ %s: Capton' % dict('Author'))
      elif line == 5:
          print('。  @ %s: http://ccapton.cn' % dict('Blog'))
      elif line == 4:
          print('。  @ %s: chenweibin1125@foxmail.com' % dict('Email'))
      elif line == 3:
          print('。  @ %s: https://github.com/ccapton' % dict('Github'))
      elif line == 2:
          print('。  @ %s: https://github.com/Ccapton/python-stuff/tree/master/filetransporter' % dict('Project'))
      else:
          print('。')
      line -= 1
    print('*'*60)

if __name__ == '__main__':
      pass


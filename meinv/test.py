#!/usr/bin/env python
# -*- coding:utf-8 -*- 
#。—————————————————————————————————————————— 
#。                                           
#。  test.py                               
#。                                           
#。 @Time    : 2018/8/1 12:56                
#。 @Author  : capton                        
#。 @Software: PyCharm                
#。 @Blog    : http://ccapton.cn              
#。 @Github  : https://github.com/ccapton     
#。 @Email   : chenweibin1125@foxmail.com     
#。__________________________________________
import os

class Mission:
    def __init__(self,start,end):
        for index in range(start,end):
            print(index)

# if __name__ == '__main__':
#    Mission(1,int(46/3))
#    Mission(int(46/3),int(46/3*2))
#    Mission(int(46/3*2),46+1)
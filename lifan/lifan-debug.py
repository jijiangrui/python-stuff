#!/usr/bin/env python
# -*- coding:utf-8 -*- 
#。—————————————————————————————————————————— 
#。                                           
#。  lifan-debug.py
#。                                           
#。 @Time    : 2018/8/1 18:08                
#。 @Author  : capton                        
#。 @Software: PyCharm                
#。 @Blog    : http://ccapton.cn              
#。 @Github  : https://github.com/ccapton     
#。 @Email   : chenweibin1125@foxmail.com     
#。__________________________________________
from lifan import run
from constant import port


if __name__ == '__main__':
    from constant import localIp
    run(localIp, port,debug=True)

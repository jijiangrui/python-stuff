#!/usr/bin/env python
# -*- coding:utf-8 -*- 
#。—————————————————————————————————————————— 
#。                                           
#。  test.py                               
#。                                           
#。 @Time    : 2018/7/26 00:09                
#。 @Author  : capton                        
#。 @Software: PyCharm                
#。 @Blog    : http://ccapton.cn              
#。 @Github  : https://github.com/ccapton     
#。 @Email   : chenweibin1125@foxmail.com     
#。__________________________________________


if __name__ ==  '__main__':
    max = 40
    index = 1
    while index <= max:
       if int(index) > 4:
          print( int(index/4) +1 )
       else:
          print('  ' + str(index))
       index +=1

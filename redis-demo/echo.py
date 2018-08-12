#coding=utf-8
#。—————————————————————————————————————————— 
#。                                           
#。  echo.py                               
#。                                           
#。 @Time    : 2018/8/9 20:35                
#。 @Author  : capton                        
#。 @Software: PyCharm                
#。 @Blog    : http://ccapton.cn              
#。 @Github  : https://github.com/ccapton     
#。 @Email   : chenweibin1125@foxmail.com     
#。__________________________________________

import requests

if __name__ =='__main__':
    import time
    running = True
    min = 5
    while running:
        try:
            response = requests.get('https://capton.herokuapp.com')
            print(response.content.decode(encoding='utf-8'))
            print('正在执行任务。。。循环周期：%d分钟' % min)
            time.sleep(60 * min)
        except KeyboardInterrupt:
            running = False
            print('退出任务')

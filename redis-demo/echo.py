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
    while True:
        response = requests.get('http://www.baidu.com')
        print(response.content.decode(encoding='utf-8'))
        time.sleep(60*5)

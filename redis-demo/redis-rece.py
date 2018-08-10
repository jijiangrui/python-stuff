#coding=utf-8
#。—————————————————————————————————————————— 
#。                                           
#。  meizi-server.py
#。                                           
#。 @Time    : 2018/8/8 18:35                
#。 @Author  : capton                        
#。 @Software: PyCharm                
#。 @Blog    : http://ccapton.cn              
#。 @Github  : https://github.com/ccapton     
#。 @Email   : chenweibin1125@foxmail.com     
#。__________________________________________
import redis
from redis import Redis
import requests
from bs4 import BeautifulSoup
from threading import Thread
import _thread
import time
import json

local_ip = '192.168.1.101'
public_ip = '111.230.231.107'
port = 6379
password = 1125

def recoding(red):
    #print('download')
    while True:
        try:
            model_json = red.lpop('model_json')
            if model_json:
                json_str = model_json.decode(encoding='utf8')
                print(json_str)
                save_record(json_str)
        except Exception as e:
            print(e)
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            print('退出')
            exit(0)



from models import IqiyiVmovieModel
from db.db_executor import DbExecutor
from datetime import datetime
def save_record(json_Str):

    vmodel = json.loads(json_Str)
    aqiyiVmodel = IqiyiVmovieModel(name=vmodel['name'],img_url=vmodel['img_url'],area=vmodel['area'],movie_type=vmodel['movie_type'],
                                   movie_standard=vmodel['movie_standard'],generation=vmodel['generation'],actors=vmodel['actors'],
                                   html_url=vmodel['html_url'],url_type=-1,url='',update_time=datetime.now())
    successful,save_type = DbExecutor().save_AqiyiVmovieModel(aqiyiVmodel)
    if successful:
        if save_type == 0:
            print('插入操作成功')
        else:
            print('更新操作成功')
    else:
        print('操作失败')


def start_listening():
    red = redis.StrictRedis(host=local_ip, port=port, password=password)
    print('已连接到数Redis据库')
    recoding(red)


if __name__ =='__main__':
    start_listening()

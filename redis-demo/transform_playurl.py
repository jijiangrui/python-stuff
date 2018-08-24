#coding=utf-8
#。—————————————————————————————————————————— 
#。                                           
#。  transform_playurl.py                               
#。                                           
#。 @Time    : 2018/8/14 21:06                
#。 @Author  : capton                        
#。 @Software: PyCharm                
#。 @Blog    : http://ccapton.cn              
#。 @Github  : https://github.com/ccapton     
#。 @Email   : chenweibin1125@foxmail.com     
#。__________________________________________

from vvideo import route_url
from db.db_transformer import get_aqiyi_moviemodels_by_area
from db.db_executor import DbExecutor

from constants import iqiayi_constants
import time


def transform(moviemodel):
    print(moviemodel.html_url)
    video_url, isVipUrl, type = route_url(moviemodel.html_url)
    if isVipUrl:
        if type == 0:
            print('video_url')
            moviemodel.url_type = 0
        elif type == 1:
            print('m3u8_url')
            moviemodel.url_type = 1
        print(video_url)
        moviemodel.url = video_url
    else:
        moviemodel.url_type = -2
        print('not vip')
    DbExecutor().save_AqiyiVmovieModel(moviemodel)
    print(moviemodel)




if __name__ == '__main__':
    for ares in  iqiayi_constants.get('areas'):
        moviemodel_list = get_aqiyi_moviemodels_by_area(ares[1],1,10,True)
        for moviemodel in moviemodel_list:
            print(moviemodel)
            if moviemodel.url_type == -1:
                transform(moviemodel)
            else:
                if moviemodel.url_type == -2:
                    continue
                print(moviemodel.name+' 已得到播放地址')
            time.sleep(1)




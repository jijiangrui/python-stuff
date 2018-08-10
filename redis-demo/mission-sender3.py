#coding=utf-8
#。—————————————————————————————————————————— 
#。                                           
#。  mission-sender3.py                               
#。                                           
#。 @Time    : 2018/8/9 13:24                
#。 @Author  : capton                        
#。 @Software: PyCharm                
#。 @Blog    : http://ccapton.cn              
#。 @Github  : https://github.com/ccapton     
#。 @Email   : chenweibin1125@foxmail.com     
#。__________________________________________
from __future__ import unicode_literals

import redis
import requests
from bs4 import BeautifulSoup
from threading import Thread
import time
import json


local_ip = '192.168.1.101'
public_ip = '111.230.231.107'
port = 6379
password = 1125

current_ip = local_ip

from constants import get_iqiyi_vmovie_list


def get_raw_videomodel_list(url, category):
    retry_times = 3
    response = None
    while retry_times > 0:
        try:
            response = requests.get(url, timeout=5)
            break
        except requests.exceptions.ReadTimeout as e:
            print(e)
            retry_times -= 1

    raw_videomodel_list = []
    if response == None:
        div = None
    else:
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            div = soup.find('div', attrs={'data-widget-listviptip': 'listviptip'})
        else:
            div = None
    try:
        li_list = div.ul.find_all('li')
        for li in li_list:
            # print(li)
            titile_p = li.find('p', attrs={'class': 'site-piclist_info_title movie-tit '})
            title = titile_p.text.replace('\n', '')
            raw_video_link = titile_p.a['href']
            img_url = 'http:' + li.find('img')['src']
            role_div = li.find('div', attrs={'class': 'role_info'})
            actors = ''
            for actor in role_div.find_all('em')[1:]:
                actors += actor.text.replace('\n', '').replace('\r', '').replace(' ', '') + ' '
            raw_videomodel_list.append((title, raw_video_link, img_url, actors, category))
    except AttributeError:
        print('此页面没有结果' + url)
    return raw_videomodel_list


def post_json_Str(red, json_str):
    red.lpush('model_json', json_str)
    print('已发送到' + current_ip)
    try:
        time.sleep(0.1)
    except KeyboardInterrupt:
        print('退出')
        exit(0)


def send(sender_index):
    if sender_index < 1 or sender_index > 3:
        print('不可用的任务序号')
        return
    red = redis.StrictRedis(host=current_ip, port=port, password=password)

    # for index in range(int((sender_index - 1) * len(get_iqiyi_vmovie_list(1)[0]) / 3),
    #                     int(sender_index * len(get_iqiyi_vmovie_list(1)[0]) / 3)):
    for index in range(int((sender_index - 1) * len(get_iqiyi_vmovie_list(1)[0]) / 3),
                       int(sender_index * len(get_iqiyi_vmovie_list(1)[0]) / 3)):
        print('当前序号：%s'% index)
        model_list = get_raw_videomodel_list(get_iqiyi_vmovie_list(1)[0][index], get_iqiyi_vmovie_list(1)[1][index])
        for model in model_list:
            print(model)
            model_json = {
                'name': model[0],
                'html_url': model[1],
                'img_url': model[2],
                'actors': model[3],
                'area': model[4].split(' ')[0],
                'movie_type': model[4].split(' ')[1],
                'movie_standard': model[4].split(' ')[2],
                'generation': model[4].split(' ')[3],
            }
            post_json_Str(red, json.dumps(model_json,ensure_ascii=False))
        time.sleep(0.1)

if __name__ == '__main__':
    send(3)
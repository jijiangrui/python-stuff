#!/usr/bin/env python
# -*- coding:utf-8 -*- 
#。—————————————————————————————————————————— 
#。                                           
#。  vvideo.py                               
#。                                           
#。 @Time    : 2018/8/2 13:48                
#。 @Author  : capton                        
#。 @Software: PyCharm                
#。 @Blog    : http://ccapton.cn              
#。 @Github  : https://github.com/ccapton     
#。 @Email   : chenweibin1125@foxmail.com     
#。__________________________________________

import requests
from bs4 import BeautifulSoup

base_url = 'http://yun.baiyug.cn/'
index_url = 'http://yun.baiyug.cn/vip/index.php?url='
app_url = 'http://cms.baiyug.cn/vip/app.php?url='

import sys,os
savepath = 'file'

def Headers (referer=''):
    return  {
    'Referer':referer,
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
}

def route_url(video_html_url):
    url = app_url + video_html_url
    header = Headers(index_url + video_html_url)
    response = requests.get(url,headers=header)
    #print(response.content.decode(encoding='utf8'))
    soup = BeautifulSoup(response.content,'html.parser')
    iframe = soup.find('iframe',attrs={'id':'api'})
    url2 = iframe['src']
    header2 = Headers(url)
    response2 = requests.get(url2,headers=header2)
    #print(response2.content.decode(encoding='utf8'))
    soup2 = BeautifulSoup(response2.content,'html.parser')
    iframe2 = soup2.find('iframe',attrs={'id':'baiyug'})
    url3 = iframe2['src']
    header3 = Headers(url2)
    response3 = requests.get(url3,headers=header3)
    html_text = response3.content.decode(encoding='utf8')
    video_url = match_url(html_text)
    if video_url:
        return video_url,True
    return index_url + video_html_url.split('#')[0] , False

def match_base_url(text):
    import re
    res = re.search('http.+\';',text)
    return res.group()[:len(res.group())-len('\';')]

def match_last_api(text):
    import re
    res = re.search('".+\.php"', text)
    return res.group()[1:len(res.group())-1]

def match_url(text):
    import re
    res = re.search('http.+\" controls=',text)
    if not res:
        return None
    if not res.group():
        return None
    elif len(res.group()) == 0 or ((not res.group().startswith('http://')) and (not res.group().startswith('https://'))):
        return None
    return res.group()[:len(res.group())-len('\" controls=')]

def get_video_headers(url):
    response = requests.head(url)
    return response.headers






if __name__ == '__main__':
    # http://www.iqiyi.com/v_19rr88lqag.html 普通视频 脑死亡第1集
    # http://www.iqiyi.com/v_19rr88mnx8.html#curid=768073200_f8b225c6860c84efb01018d6772c4f4f 普通视频 脑死亡第2集
    # http://www.iqiyi.com/v_19rr88son0.html#curid=768238800_7d51e964156bb462dde89eddeafa1080 VIP视频 脑死亡第10集
    video_url,isVipUrl = route_url('https://v.youku.com/v_show/id_XMTU2ODE4OTczNg==.html?spm=a2h0j.11185381.listitem_page1.5!3~A&&s=920240a0db7211e58bfb')
    if not isVipUrl:
        print('不是VIP视频')
        print(video_url)
    else:
        print(video_url)


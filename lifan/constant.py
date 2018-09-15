#!/usr/bin/env python
# -*- coding:utf-8 -*- 
#。—————————————————————————————————————————— 
#。                                           
#。  constant.py  各种常量
#。                                           
#。 @Time    : 2018/8/3 19:23                
#。 @Author  : capton                        
#。 @Software: PyCharm                
#。 @Blog    : http://ccapton.cn              
#。 @Github  : https://github.com/ccapton     
#。 @Email   : chenweibin1125@foxmail.com     
#。__________________________________________

# 图片保存路径
image_save_path = 'static/img/cover'

# peewee数据库文件保存路径
db_save_path = 'db/data'

'''
若你的vps只有一个公网ip，则ip,publicIP都设置为这一个公网ip值
若有公网ip和内网ip则，开启web服务器时用内网ip
'''
ip = '10.135.120.137'         # vps虚拟云主机内网ip
publicIP = '111.230.231.107'  # vps虚拟云主机公网ip
localIp = '0.0.0.0'           # 公共ip，供局域网内用户访问

psw = 666
port = 5050

debug = True

base_host = 'http://demo.lvmaojun.com/web07'
index_url = 'http://demo.lvmaojun.com/web07/index.php'  # 首页
categories = 'http://demo.lvmaojun.com/web07/index.php?category=0' # 里番分类
category_url = 'http://demo.lvmaojun.com/web07/index.php?category='

'''
Cookie 灰常重要，如果访问受阻了，请尝试用手机重新登录浏览app，以抓包获取你个人账号对应的cookie
'''
Cookie = 'web_client=android; web_temp=4c099y7reggc4nwi3qre5s1536942308; web_id=164807; web_key=t8k8k4dwson1mt63aedk4v1536942368'
UserAgent = 'Mozilla/5.0 (Linux; Android 7.1.2; MI 5X Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 ' \
            'Chrome/67.0.3396.87 Mobile Safari/537.36'

Headers = {
    'Cookie':Cookie,
    'User-Agent':UserAgent,
}

"""
  设置当前ip ，若开发环境，则 currentIp = localIp，否则 currentIp = publicIP
"""
# currentIp = publicIP # 当前ip设置为公网ip
currentIp = localIp # 当前ip设置为本地ip

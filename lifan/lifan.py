#!/usr/bin/env python
# -*- coding:utf-8 -*- 
#。—————————————————————————————————————————— 
#。                                           
#。  lifan.py   对外提供接口
#。                                           
#。 @Time    : 2018/8/3 13:51                
#。 @Author  : capton                        
#。 @Software: PyCharm                
#。 @Blog    : http://ccapton.cn              
#。 @Github  : https://github.com/ccapton     
#。 @Email   : chenweibin1125@foxmail.com     
#。__________________________________________

from flask import Flask,Response,url_for
from flask_restful import Api
from lifan_api import LifanResource

import os

from constant import ip,port
from constant import image_save_path

app = Flask(__name__)
app.config.update(RESTFUL_JSON=dict(ensure_ascii=False)) # 中文显示json数据,ensure_ascii为True时，中文将表示为ascii码

api = Api(app)

api.add_resource(LifanResource,'/lifan/api')

@app.route('/')
def index():
    return '请跳转到 '+url_for('index')+'lifan/api'

@app.route('/img/<category>/<imgname>')
def output_img(category,imgname):
    try:
        resp = Response(open(os.path.join(image_save_path,category,imgname),'rb'), mimetype="image/jpeg")
    except:
        resp = Response(open('static/img/no_cover.jpg','rb'), mimetype="image/jpeg")
    return resp

def run(ip,port,debug=False):
    app.run(ip, port,debug=debug)

if __name__ == '__main__':
    from constant import ip,localIp
    #run(localIp,port) # 本地测试用
    run(ip,port)   # 运行在有公网ip的服务器上


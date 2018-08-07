#coding=utf-8
#。—————————————————————————————————————————— 
#。                                           
#。  stc.py  图片文件的下载，不同表数据的转移
#。                                           
#。 @Time    : 2018/8/3 22:33                
#。 @Author  : capton                        
#。 @Software: PyCharm                
#。 @Blog    : http://ccapton.cn              
#。 @Github  : https://github.com/ccapton     
#。 @Email   : chenweibin1125@foxmail.com     
#。__________________________________________

import os
from threading import Thread,Lock

import requests

from db.db_executor import *
from constant import *
from util import log

if not os.path.exists(image_save_path): os.makedirs(image_save_path)

class ImgSaverThread (Thread):
    def __init__(self,lifan_list,start_index,end_index,threadIndex):
        Thread.__init__(self)
        self.threadname = '图片下载线程'+str(threadIndex)
        self.lifan_list = lifan_list
        self.start_index = start_index
        self.end_index = end_index

    def download(self,isSmallCover=False):
        for lifan in self.lifan_list[self.start_index:self.end_index]:
            last_word = ''
            if isSmallCover:
                last_word = '_s'
                cover = lifan.cover_s
            else:
                cover = lifan.cover_l
            log('%s 下载图片 %s' % (self.threadname, cover))
            img_savepath = os.path.join(image_save_path, lifan.category)
            if not os.path.exists(img_savepath):
                os.makedirs(img_savepath)
            filepath = os.path.join(img_savepath, lifan.title + last_word + '.jpg')
            if os.path.exists(filepath):
                log('图片' + filepath + ' 已存在')
                continue
            with open(filepath, 'wb') as f:
                res = requests.get(cover, headers=Headers)
                if res.status_code == 200:
                    f.write(res.content)
                log('图片下载完成 ' + filepath)

    def run(self):
        try:
            self.download(True)
        except:
            pass
        try:
            self.download(False)
        except:
            pass



class DataMigrater:
    def __init__(self):
        self.serverLifanExecutor = ServerLifanExecutor()
        self.clientLifanExecutor = ClientLifanExecutor()

    def update_local_imgs(self,all,ip=currentIp,category_index=None):
        if not category_index:
            if len(CategoryExecutor().get_all_category()) == 0:
                print('先下载目录')
                return
            else:
                category_index = CategoryExecutor().get_all_category()[0].index
        if all:
            categories = CategoryExecutor().get_all_category()
            log('更新全部目录')
        else:
            categories = CategoryExecutor().query_category_by_index(category_index,True)
            log('更新目录 '+str(category_index))
        for category in categories:
            lifanS_list = self.serverLifanExecutor.query_lifanS_by_category(category.name,all=True)
            for lifanS in lifanS_list:
                last_word = '_s'
                lifanS.cover_s = 'http://'+ip+':'+str(port)+'/img/'+lifanS.category+'/'+ lifanS.title + last_word + '.jpg'
                lifanS.cover_l = 'http://'+ip+':'+str(port)+'/img/'+lifanS.category+'/'+ lifanS.title  + '.jpg'
                lifanC = LifanC(title=lifanS.title,category=lifanS.category,magnet=lifanS.magnet,
                                cover_s=lifanS.cover_s,cover_l=lifanS.cover_l,index=lifanS.index)
                success, type = self.clientLifanExecutor.save_lifanC(lifanC)
                if success:
                    if type == 0:
                        log('客户端数据保存完成'+lifanC.title)
                    else:
                        log('客户端数据更新完成'+lifanC.title)
                else:
                    if type == 0:
                        log('客户端数据保存失败！'+lifanC.title)
                    else:
                        log('客户端数据更新失败！'+lifanC.title)

    def download_remote_imgs(self,all,category_index=None,threadNum=10):
        if not category_index:
            if len(CategoryExecutor().get_all_category()) == 0:
                print('先下载目录')
                return
            else:
                category_index = CategoryExecutor().get_all_category()[0].index
        if not all:
            categories = CategoryExecutor().query_category_by_index(category_index,True)
        else:
            categories = CategoryExecutor().get_all_category()

        for category in categories:
            lifanS_list = self.serverLifanExecutor.query_lifanS_by_category(category.name,all=True)
            thread_list= []
            for threadIndex in range(0,threadNum):
                imgSaverT = ImgSaverThread(lifanS_list,
                                           int(threadIndex * len(lifanS_list)/threadNum),
                                           int((threadIndex + 1)* len(lifanS_list)/threadNum),
                                           threadIndex)
                imgSaverT.start()
                thread_list.append(imgSaverT)
            for t in thread_list:
                t.join()
                log(t.threadname+' 任务完成')
            log(category.name+' 图片下载任务完成')






#if __name__ == '__main__':
    #ImageMigrater().download_remote_imgs()





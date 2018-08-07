#coding=utf-8
#。—————————————————————————————————————————— 
#。                                           
#。  spider.py  爬虫主体程序
#。                                           
#。 @Time    : 2018/8/3 13:53                
#。 @Author  : capton                        
#。 @Software: PyCharm                
#。 @Blog    : http://ccapton.cn              
#。 @Github  : https://github.com/ccapton     
#。 @Email   : chenweibin1125@foxmail.com     
#。__________________________________________ 

import time
from threading import Thread,Lock

import requests
from bs4 import BeautifulSoup

from db.db_executor import *
from constant import *
import constant
from util import formated_time,log

from stc import DataMigrater


class MissionManager:
    def __init__(self,category,threadNum=3,l_list=None):
        self.category = category
        if threadNum >0 and threadNum <= 10:
            self.threadNum = threadNum
        else:
            self.threadNum = 3
        self.l_list = l_list
        self.multThread = True
        self.threadLock = Lock() # 线程锁，用于数据库写入操作同步进行，防止异步操作造成数据写入报错
        self.complishedNum = 0

    # 任务分发
    def dispatch(self):
        t_list = [] # 线程列表

        if self.multThread:
            if len(self.l_list) / self.threadNum > 1:
                for i in range(0, self.threadNum):
                    # 平均分配给每条线程 任务总数/线程数 的工作量
                    sm = SpiderMan('线程' + str(i),
                                   self.category,
                                   int(i / self.threadNum * len(self.l_list)),
                                   int((i + 1) / self.threadNum * len(self.l_list)),
                                   self.l_list)
                    sm.setMissionManager(self)
                    sm.threadLock = self.threadLock
                    sm.start()
                    t_list.append(sm)
            else:
                sm = SpiderMan('单线程', self.category, 0, len(self.l_list), self.l_list)
                sm.setMissionManager(self)
                sm.start()
                t_list.append(sm)
        else:
            sm = SpiderMan('单线程', self.category, 0, len(self.l_list), self.l_list)
            sm.setMissionManager(self)
            sm.start()
            t_list.append(sm)

        for t in t_list:
            try:
                t.join()
            except:
                t.working = False
                log('[任务中断]')
                log('[任务结束中]')
        log('[任务结束] 更新了'+str(self.complishedNum)+'项')


class SpiderMan(Thread):
    def __init__(self,t_name,category,start_index,end_index,l_list):
        Thread.__init__(self)
        self.t_name = t_name
        self.category = category
        self.start_index = start_index
        self.end_index = end_index
        self.l_list = l_list
        self.threadLock = None
        self.missionManager = None
        self.working = True

    # 获取soup对象
    def getSoup(self,url):
        response = requests.get(url, headers=Headers)
        return BeautifulSoup(response.content, 'html.parser')

    def setMissionManager(self,manager):
        self.missionManager = manager

    def do_work(self,index):
        lifanS = LifanS(category=self.category, title=self.l_list[index][0], index=index,cover_s=self.l_list[index][1])
        import random
        time.sleep(0.1 * random.random())
        detail_url = self.l_list[index][2]
        log('[%s]' % self.category + detail_url)
        soup2 = self.getSoup(detail_url)
        cover_l = match_coverL(soup2.find('div', attrs={'id': 'img-box'})['style'])
        magnet = soup2.find('div', attrs={'class': 'video-desc'}).text
        lifanS.cover_l = cover_l
        lifanS.magnet = magnet
        log(self.t_name + ' ' + str(lifanS))

        if self.threadLock: self.threadLock.acquire()
        res = ServerLifanExecutor().save_lifanS(lifanS)
        if res[0]:
            if res[1] == 0:
                log(lifanS.title + ' 插入成功')
            else:
                log(lifanS.title + ' 更新成功')
            if self.missionManager:
                self.missionManager.complishedNum += 1
        else:
            log(lifanS.title + ' 操作失败')
        if self.threadLock: self.threadLock.release()


    def run(self):
        for index in range(self.start_index, self.end_index):
            if self.working:
                self.do_work(index)

# 获取soup对象
def getSoup(url):
    response = requests.get(url, headers=Headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


# 获取最新里番
def download_newest(multThread=True,threadNum=6):
    if len(CategoryExecutor().get_all_category()) == 0:
        print('先下载目录')
        return
    index = str (CategoryExecutor().get_all_category()[0].index)
    category_name = str (CategoryExecutor().get_all_category()[0].name)
    newest_url = category_url + index
    download_all_lifan_in_category(newest_url,category_name,multThread,threadNum)

# 获取过去(2017年及以前)的
def download_past(multThread=True,threadNum=6):
    for category in CategoryExecutor().get_all_category()[1:]:
         category_past_url = category_url + str( category.index )
         download_all_lifan_in_category(category_past_url,category.name,multThread,threadNum)

# 下载指定目录的里番
def download_lifan_by_index(index,multThread=True,threadNum=6):
    for category in CategoryExecutor().get_all_category():
        if index == category.index:
            category_past_url = category_url + str(category.index)
            download_all_lifan_in_category(category_past_url, category.name, multThread, threadNum)


# 下载目录列表
def download_categories():
    url = categories
    items = getSoup(url).find_all('a',attrs={'class':'act-item'})
    for item in items:
        import re
        index = int(re.search('\d+',item['href']).group())
        name = item.span.text
        success , type = CategoryExecutor().save_category(Category(index=index,name=name))
        if success:
            if type == 0:
                log(str(index)+ ' ' + name + ' 插入成功')
            else:
                log(str(index)+ ' ' + name + ' 更新成功')


# 展示所有目录
def show_categories():
     categories = CategoryExecutor()._get_all_category()
     for category in categories:
         log(category)
     if len(categories) == 0:
         log('没有下载目录请使用 -cate 指令')


# 获取目录下的所有里番信息，并逐一爬取对应的磁力链、图片地址
def download_all_lifan_in_category(url,category,multThread=True,threadNum=6):
    log(url)
    a_list = getSoup(url).find_all('a', attrs={'class': 'list-item'})
    log('番数：'+str(len(a_list)))
    l_list = [] # 元祖列表（标题，小封面，详情链接）
    for item in a_list:
        cover_img_small = item.find('div', attrs={'class': 'cover-img lazy'})['data-original']
        title = item.find('div', attrs={'class': 'title'}).text
        link = item['href']
        l_list.append( (title, cover_img_small, base_host+'/'+link) ) #  添加元祖（标题，小封面，详情链接）

    missionManager = MissionManager(category,threadNum,l_list) # 初始化任务管理类
    missionManager.multThread = multThread # 单线程或多线程
    missionManager.dispatch()

# 匹配链接
def match_coverL(text):
    import re
    res = re.search('http.+\);',text)
    return res.group()[:len(res.group())-len(');')]

# 循环任务类
class RecycleTask(Thread):

    # 循环定时任务回调类，用于被继承，doMission内执行具体的任务代码
    class MissionCallback:
        def doMission(self):
            pass

    def __init__(self,name = '',missionCallback=None,interval = 3600):
        Thread.__init__(self)
        self.name = name
        self.missionCallback = missionCallback
        self.interval = interval
        self.working = True
        self.left_second = self.interval


    def start_mission(self):
        if self.missionCallback:
            self.missionCallback.doMission()

    def run(self):
        log('开始 ' + self.name + ' 循环任务')
        try:
            self.start_mission()
        except:
            self.working = False
        while self.working:
            import sys
            self.left_second -= 1
            if self.left_second >= 0:
                import time
                sys.stdout.write('距离下次任务，还有' + formated_time(self.left_second) + '\r')
                time.sleep(1)
            else:
                log('')
                self.left_second = self.interval
                try:
                    self.start_mission()
                except:
                    self.working = False
                    break

# 继承自 循环定时任务回调类 RecycleTask.MissionCallback doMission内执行任务
class MyWork(RecycleTask.MissionCallback):
    def doMission(self):
        download_categories() # 获取所有目录
        download_newest(True) # 获取最新里番
        DataMigrater().update_local_imgs(False)
        DataMigrater().download_remote_imgs(all = False, category_index = CategoryExecutor().get_all_category()[0].index)


def delete_all_in_client_db():
    for category in CategoryExecutor().get_all_category():
        executor = ClientLifanExecutor()
        res = executor.delete_lifanC_by_category(category.name)
        if res:
            log('删除成功')
        else:
            log('删除失败')


def delete_all_in_server_db():
    for category in CategoryExecutor().get_all_category():
        executor = ServerLifanExecutor()
        res = executor.delete_lifanS_by_category(category.name)
        if res:
            log('删除成功')
        else:
            log('删除失败')

if __name__ == '__main__':
    #get_past(True)
    #  RecycleTask('爬取最新里番', MyWork(), 20).start()

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-newest', '--newest', required=False,help='爬取最新里番')
    parser.add_argument('-newest_r', '--newest_r', required=False,help='循环爬取最新里番')
    parser.add_argument('-all', '--all', required=False,help='爬取所有里番')
    parser.add_argument('-index', '--index', type=int,required=False,help='爬取指定目录的里番')
    parser.add_argument('-cate', '--cate', required=False,help='爬取目录')
    parser.add_argument('-showcate', '--showcate', required=False,help='展示目录')
    parser.add_argument('-img', '--image', required=False,help='下载所有图片')
    parser.add_argument('-img_index', '--image_index', required=False,help='下载指定目录的图片')
    parser.add_argument('-update', '--update', required=False,help='更新客户数据库')
    parser.add_argument('-update_index', '--update_index', required=False,help='更新指定目录的客户数据库')
    parser.add_argument('-showc', '--showc', required=False,help='显示所有客户数据')
    parser.add_argument('-shows', '--shows', required=False,help='显示所有原始数据')
    parser.add_argument('-delc', '--delc', type=int,required=False,help='删除客户端数据')
    parser.add_argument('-dels', '--dels', type=int,required=False,help='删除服务端数据')
    parser.add_argument('-auto', '--auto', type=int,required=False,help='自动化完成全部')

    args = parser.parse_args()

    if args.newest:
        download_newest(True)
    elif args.newest_r != None:
        RecycleTask('爬取最新里番', MyWork(), 3600*24).start()
    elif args.all:
        download_newest(True)
        download_past(True)
    elif args.image:
        DataMigrater().download_remote_imgs(True)
    elif args.image_index:
        DataMigrater().download_remote_imgs(False,args.image_index)
    elif args.update:
        DataMigrater().update_local_imgs(True)
    elif args.update_index:
        DataMigrater().update_local_imgs(False,args.update_index)
    elif args.showc:
        for category in CategoryExecutor().get_all_category():
            lifanC_list = ClientLifanExecutor().query_lifanC_by_category(category.name, all=True)
            for lifanC in lifanC_list:
                log(lifanC)
    elif args.shows:
        for category in CategoryExecutor().get_all_category():
            lifanS_list = ServerLifanExecutor().query_lifanS_by_category(category.name, all=True)
            for lifanS in lifanS_list:
                log(lifanS)
    elif args.delc:
        if args.delc == psw:
            delete_all_in_client_db()
        else:
            log('密码错误,操作密码为：'+str(psw))
    elif args.dels:
        if args.dels == psw:
            delete_all_in_server_db()
        else:
            log('密码错误,操作密码为：'+str(psw))
    elif args.cate:
        download_categories()
    elif args.showcate:
        show_categories()
    elif args.index:
        if isinstance(args.index,int):
            download_lifan_by_index(args.index)
        else:
            log('请输入数字')
    elif args.auto:
        if args.auto == psw:
             download_categories()
             download_newest(True)
             download_past(True)
             DataMigrater().update_local_imgs(True)
             DataMigrater().download_remote_imgs(True)
        else:
            log('密码错误,操作密码为：'+str(psw))
    else:
        parser.print_help()


#coding:utf-8
#。—————————————————————————————————————————— 
#。                                           
#。  jiandan.py  爬取煎蛋网女生图片
#。  本程序由于要模拟浏览器(网页元素是由js生成的，so只能模拟)行为，
# 可能速度会很慢，请谅解
#。                                           
#。 @Time    : 2018/8/1 10:10                
#。 @Author  : capton                        
#。 @Software: PyCharm                
#。 @Blog    : http://ccapton.cn              
#。 @Github  : https://github.com/ccapton     
#。 @Email   : chenweibin1125@foxmail.com     
#。__________________________________________

from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import re
from threading import Thread
import os,sys
import time

savepath='/users/capton/downloads/jiandan' # 图片保存路径

class JianDan:
    def __init__(self):
        self.base_url = 'http://i.jandan.net/ooxx'
        self.max_page_num = self.get_max_page_num()
        print('页码数 %d' % self.max_page_num)
        self.current_url = ''
        self.start_index = 1
        if not os.path.exists(savepath):
            os.makedirs(savepath)

    def Header(self,**args):
        return {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
            'Host': args.get('host'),
        }

    def get_max_page_num(self):
        try:
            response = requests.get(self.base_url)
            if response.status_code == 200:
                content = response.content
                soup = BeautifulSoup(content, 'html.parser')
                num_text = soup.find('span', attrs={'class': 'current-comment-page'}).text
                num = re.search('\d+', num_text).group()
                return int(num)
        except Exception:
            pass
        return 0

    def start_download(self):
        if self.max_page_num == 0:
            print('页码数为0')
            return
        else:
            threads = []
            # 文件下载地址 http://phantomjs.org/download.html，放置本文件jiandan.py同目录
            worker1 = Worker('线程1',1,int(self.max_page_num /3 ))
            worker2 = Worker('线程2',int(self.max_page_num /3 ),int(self.max_page_num /3 * 2))
            worker3 = Worker('线程3',int(self.max_page_num /3 * 2),self.max_page_num + 1)
            worker1.start()
            worker2.start()
            worker3.start()
            threads.append(worker1)
            threads.append(worker2)
            threads.append(worker3)
            for t in threads:
                t.join()
            print('任务完成') 



class Worker(Thread):
    def __init__(self,name,start_index,end_index):
        Thread.__init__(self)
        self.name = name
        self.start_index = start_index
        self.end_index = end_index
        self.planthomjs = webdriver.PhantomJS()

    def get_url(self,page):
        return 'http://i.jandan.net/ooxx/page-%d#comments' % page

    def get_html(self,page):
        print(self.get_url(page))
        self.planthomjs.get(self.get_url(page))
        source_html = self.planthomjs.page_source
        soup = BeautifulSoup(source_html, 'html.parser')
        commentlist = soup.find('ol', attrs={'class': 'commentlist'})
        return commentlist

    def get_pic_urls(self,soup_object):
        pic_urls = []
        text_list = soup_object.find_all('div',attrs={'class':'text'})
        for text in text_list:
            if text.p.img:
               img_url = text.p.img['src']
               pic_urls.append(img_url)
            else:
               img_urls = text.img
               pic_urls.extend(img_urls)
        return pic_urls

    def run(self):
        print(self.name+'开启')
        for page in range(self.start_index,self.end_index):
            html_str = self.get_html(page)
            img_list = self.get_pic_urls(html_str)
            threads = []
            for img_url in img_list:
                imgSaverThread = ImgSaverThread(self.name,page,img_url)
                imgSaverThread.start()
                threads.append(imgSaverThread)
                time.sleep(0.05)
            for t in threads:
                t.join()
            print('%s 第%d页图片保存完毕' % (self.name,page))
            time.sleep(0.2)
        self.planthomjs.quit()


class ImgSaverThread (Thread):
    def __init__(self,threadname,page,img_url):
        Thread.__init__(self)
        self.img_url = img_url
        self.threadname = threadname
        self.page = page
        self.page_path = os.path.join(savepath, str(self.page))
        if not os.path.exists(self.page_path):
            os.makedirs(self.page_path)

    def run(self):
        print('%s 下载第%d页图片 %s' % (self.threadname,self.page,self.img_url))
        filepath = os.path.join(self.page_path,os.path.basename(self.img_url))
        if os.path.exists(filepath):
            print('图片'+filepath+'已存在')
            return
        with open(filepath,'wb') as f:
            res = requests.get(self.img_url)
            if res.status_code == 200:
                f.write(res.content)
            else:
                print('图片访问受限')


# 判断输入的路径是文件还是文件夹、或是否存在
def checkfile(path):
    if not path:
        return False,-1
    import os
    if os.path.isfile(path):
        return True, 1
    elif os.path.isdir(path):
        return True, 0
    else:
        return False, -1

if __name__ == '__main__':
     path = input('请输入文件的保存路径：')
     if checkfile(path)[0] and checkfile(path)[1] == 0:
         savepath = path
         print(savepath)
         JianDan().start_download()
     else:
         if checkfile(path)[0] and checkfile(path)[1] == 1:
             print('请输入文件夹路径，不是文件路径')
         else:
             print('没有此路径')





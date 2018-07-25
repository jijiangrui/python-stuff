#encoding:utf-8
  
from bs4 import BeautifulSoup
import requests
 
import os

import platform
import threading

import sys

import time

import argparse


base_url = 'https://www.meitulu.com/search/'
headers = {
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Mobile Safari/537.36',
    'Referer':''
}


linux_darwin_save_path = '/Users/capton/desktop/美女/'
windows_save_path = 'C:/美女/'

multThread = True

remainNum = 0
 
def searchMeinv(keyword):

    print(platform.platform())
    if platform.platform().find('Windows') != -1:
        base_save_path = windows_save_path
    else:
        base_save_path = linux_darwin_save_path
    print('图片保存根目录 %s' % (base_save_path))
 
    if not keyword:
        return '<h3>请输入关键词</h3>'
    final_url = base_url + keyword
    headers['Referer'] = final_url

    response = requests.get(final_url,headers)

    soup = BeautifulSoup(response.content, 'html.parser')
    main = soup.find('div',attrs={'class':'main'})
    img_ul = main.find('ul',attrs={'class':'img'})
    imgs_li = img_ul.find_all('li')

    startTime = time.time()

    if len(imgs_li) == 0:
        print('没有结果')  
    for li in imgs_li:
        html_url = li.find('a')['href']
        print(html_url)
        conver_imag_url = li.find('a').find('img')['src']
        print(conver_imag_url)
        numText = li.find('p').text
        title = li.find('p',attrs={'class':'p_title'}).find('a').text
        print('%s %s张' % (newTitleName(title),getNum(numText)))
        savePath = base_save_path + keyword
        if not os.path.exists(savePath):
            os.makedirs(savePath)

        savePath2 = savePath + '/' + newTitleName(title)
        if not os.path.exists(savePath2):
            os.makedirs(savePath2)

        downloadGalary(html_url,conver_imag_url,int(getNum(numText)),keyword,savePath2,startTime)

def newTitleName(title):
    return str(title).replace('/','_')

# 数量：61 张(1600X2400)
def getNum(numText):
    start = str(numText).find('数量： ') + 4
    end = str(numText).find('张') - 1
    return int(numText[start:end])

def newUrl(oldUrl,index):
    return str(oldUrl).replace('/0.','/'+index+'.')

def downloadGalary(referer,url,num,keyword,savePath2,startTime):

    if multThread and float(num / 3) > 1:
       MyThread(1,'线程1',1,int(num / 3),referer,url,num,keyword,savePath2,startTime).start()
       MyThread(2,'线程2',int(num / 3),int(num * 2/ 3),referer,url,num,keyword,savePath2,startTime).start()
       MyThread(3,'线程3',int(num * 2/ 3),num,referer,url,num,keyword,savePath2,startTime).start()
    else:       
       for i in range(1,num):
           pic_url = newUrl(url,str(i))
           saveImage('唯一线程',pic_url,newRefer(referer,i),keyword,savePath2)
       endTime = time.time()
       costedTime = endTime - startTime
       print('花费时间：' + str(costedTime))
       print('完成相册 ' + url)

def newRefer(html_url,index):
    if int(index) > 1:
        return str(html_url).replace('.html','_'+str(index)+'.html')
    else:
        return html_url

def newName(url):
     start = str(url).find('img/',0,len(url))
     if start == -1 :
         return ''
     else:
         tempName = str(url [ start : len(url) ] )
         finalName = str(tempName).replace('/','_')
         return finalName
 
def saveImage(threadName,target,referer,keyword,savePath2):
   if not target:
         return '<h3>请输入图片地址</h3>'
   else:
         headers['Referer'] = referer

         imgPath = savePath2+'/'+ keyword +'_' + newName(target)
         if not os.path.exists(imgPath):
                try:
                    response = requests.get(target, headers=headers)
                    pic = response.content
                    fp = open(imgPath, 'wb')
                    fp.write(pic)
                    fp.close()
                    print(threadName+' '+target + '下载成功,保存名：'+ keyword +'_' + newName(target))
                except:
                    print(threadName+' '+keyword +'_' + newName(target)+ '保存异常')
         else:
                print(threadName+' '+target + ' 已下载 '+ keyword +'_' + newName(target) + '已存在')


def rename(path,actorName):
    filelist = os.listdir(path)  # 该文件夹下所有的文件（包括文件夹）
    for files in filelist:  # 遍历所有文件
        Olddir = os.path.join(path, files);  # 原来的文件路径
        if os.path.isdir(Olddir):  # 如果是文件夹则跳过
            continue;
        filename = actorName + '_'+ os.path.splitext(files)[0];  # 文件名
        filetype = os.path.splitext(files)[1];  # 文件扩展名
        Newdir = os.path.join(path, filename + filetype);  # 新的文件路径
        os.rename(Olddir, Newdir)  # 重命名
        print(filename + filetype)


def addActorName():
    targetDir = 'F:\data'

    list = os.listdir(targetDir)  # 列出文件夹下所有的目录与文件

    for i in range(0, len(list)):

        path = os.path.join(targetDir, list[i])

class MyThread(threading.Thread):
    def __init__(self,threadId,name,startIndex,endIndex,
    referer,url,num,keyword,savePath2,startTime):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.name = name
        self.startIndex = startIndex
        self.endIndex = endIndex
        self.referer = referer
        self.url = url
        self.num = num
        self.keyword = keyword
        self.savePath2 = savePath2
        self.startTime = startTime

    def run(self):
       for i in range(self.startIndex,self.endIndex):
           pic_url = newUrl(self.url,str(i))
           saveImage(self.name,pic_url,newRefer(self.referer,i),self.keyword,self.savePath2)


def print_author_info(program_name):
    print('*'*60)
    line = 9
    while line > 0:
      if line == 8:
          print('。  %s' % program_name)
      elif line == 6:
          print('。  @ %s: Capton' % 'Author')
      elif line == 5:
          print('。  @ %s: http://ccapton.cn' % 'Blog')
      elif line == 4:
          print('。  @ %s: chenweibin1125@foxmail.com' % 'Email')
      elif line == 3:
          print('。  @ %s: https://github.com/ccapton' % 'Github')
      elif line == 2:
          print('。  @ %s: https://github.com/Ccapton/python-stuff/tree/master/meinv' % 'Project')
      else:
          print('。')
      line -= 1
    print('*'*60)


if __name__ == '__main__':

    print_author_info('美女图片下载程序'+ '  ' +'数据源：'+base_url)

    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--keyword', required=False, help=('关键词'))
    parser.add_argument('-m', '--mult_thread', required=False, help=('多线程'), type=int)

    args = parser.parse_args()

    if args.mult_thread:
        multThread = False

    if args.keyword :
        searchMeinv(args.keyword)

    else:
        keyword = input('输入关键词:')
        searchMeinv(keyword)

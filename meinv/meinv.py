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

def Headers(referer):
    return {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Mobile Safari/537.36',
        'Referer': referer
    }


save_path = 'downloads/美女'

multThread = True

remainNum = 0

all_result = False
 
def searchMeinv(keyword):
    global save_path
    save_path.replace(anti_dir_divider(),dir_divider())
    if save_path.endswith(dir_divider()):
        save_path = save_path[0:len(save_path)-1]
    print('图片保存根目录 %s' % (save_path))

    final_url = base_url + keyword

    response = requests.get(final_url,headers)

    soup = BeautifulSoup(response.content, 'html.parser')
    main = soup.find('div',attrs={'class':'main'})
    img_ul = main.find('ul',attrs={'class':'img'})
    imgs_li = img_ul.find_all('li')

    startTime = time.time()

    if len(imgs_li) == 0:
        print('没有结果')
        main_menu()
    for li in imgs_li:
        html_url = li.find('a')['href']
        print(html_url)
        if all_result:
            getGallaryPage(html_url,keyword)
            break
        conver_imag_url = li.find('a').find('img')['src']
        print(conver_imag_url)
        numText = li.find('p').text
        title = li.find('p',attrs={'class':'p_title'}).find('a').text
        print('%s %s张' % (newTitleName(title),parseNum(numText)))
        savePath = save_path + dir_divider() + keyword
        if not os.path.exists(savePath):
            os.makedirs(savePath)

        savePath2 = savePath + dir_divider() + newTitleName(title)
        print(savePath2)
        if not os.path.exists(savePath2):
            os.makedirs(savePath2)

        downloadGalary(html_url,conver_imag_url,int(parseNum(numText)),keyword,savePath2,startTime)


def getGallaryPage(url,keyword):
    headers['Referer']='https://www.meitulu.com/'
    response = requests.get(url, headers)
    if response.status_code == 200:
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            c_l = soup.find('div', attrs={'class': 'c_l'})
            p_list = c_l.find_all('p')
            for p in p_list:
                if str(p.text).find('模特姓名') != -1:
                    if p.find('a'):
                        target_url = p.find('a')['href']
                        getModelPage(target_url, keyword)
                    else:
                        print('该模特作品较少，返回部分下载模式')
                        global all_result
                        all_result = False
                        searchMeinv(keyword)
        except Exception:
            print('解析有问题')
    else:
        print('getGallaryPage '+ url +' bad response code: '+response.status_code)
        print('getGallaryPage '+ url +' bad response content : '+response.content)

def getModelPage(url,keyword):
    headers['Host'] = 'www.meitulu.com'
    response = requests.get(url, headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        main = soup.find('div', attrs={'class': 'main'})
        img_ul = main.find('ul', attrs={'class': 'img'})
        imgs_li = img_ul.find_all('li')
        startTime = time.time()
        print('套图数：%d' % len(imgs_li))
        for li in imgs_li:
            html_url = li.find('a')['href']
            conver_imag_url = li.find('a').find('img')['src']
            title = li.find('p',attrs={'class':'p_title'}).text
            numText = li.find('p').text
            num = parseNum(numText)
            print('%s %s张' % (newTitleName(title), num))
            savePath = save_path + keyword
            if not os.path.exists(savePath):
                os.makedirs(savePath)

            savePath2 = savePath + '/' + newTitleName(title)
            if not os.path.exists(savePath2):
                os.makedirs(savePath2)

            downloadGalary(html_url, conver_imag_url, num, keyword, savePath2, startTime)
    else:
        print('getModelPage ' + url + ' bad response code: ' + response.status_code)
        print('getModelPage ' + url + ' bad response content : ' + response.content)

import re
def parseNum(text):
    return  int(re.search('\d+',text).group())

def newTitleName(title):
    return str(title).replace(dir_divider(),'_')

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
       print('完成相册 ' + url)
       main_menu()


def newRefer(html_url,index):
    if int(index) > 4:
        if index % 4 != 0:
           last =  int(index / 4) + 1
        else:
           last =  int(index / 4)
        return str(html_url).replace('.html','_%d.html' % last)
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
         return
   else:
         headers = Headers(referer)
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
            continue
        filename = actorName + '_'+ os.path.splitext(files)[0];  # 文件名
        filetype = os.path.splitext(files)[1]  # 文件扩展名
        Newdir = os.path.join(path, filename + filetype);  # 新的文件路径
        os.rename(Olddir, Newdir)  # 重命名
        print(filename + filetype)


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
           self.saveImage(self.name,pic_url,newRefer(self.referer,i),self.keyword,self.savePath2)
           time.sleep(0.05)

    def saveImage(self,threadName, target, referer, keyword, savePath2):
        if not target:
            return
        else:
            headers = Headers(referer)
            imgPath = savePath2 + '/' + keyword + '_' + newName(target)
            if not os.path.exists(imgPath):
                try:
                    response = requests.get(target, headers=headers)
                    pic = response.content
                    fp = open(imgPath, 'wb')
                    fp.write(pic)
                    fp.close()
                    print(threadName + ' ' + target + '下载成功,保存名：' + keyword + '_' + newName(target))
                except:
                    print(threadName + ' ' + keyword + '_' + newName(target) + '保存异常')
            else:
                print(threadName + ' ' + target + ' 已下载 ' + keyword + '_' + newName(target) + '已存在')


def dir_divider():
    import platform
    if platform.platform().find('Windows') != -1:
        return '\\'
    else:
        return '/'


def anti_dir_divider():
    import platform
    if platform.platform().find('Windows') != -1:
        return '/'
    else:
        return '\\'

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

close_hint = '输入exit或按下Ctrl+C 退出程序'
def main_menu():
    view = '-'*25+' 主菜单 '+'-'*25 +\
           '\n 1 输入模特名开始搜索 ' +' ' * 11 + close_hint + \
           '\n 2 设置参数\n' \
            +'-'*(57)
    print(view+'\r')
    action_index = input('请选择一项： ')
    if len(action_index) == 0:
        main_menu()
    else:
        if action_index == '1':
            keyword = input('关键词：')
            if keyword.lower() == 'exit':
                exit(1)
            searchMeinv(keyword)
        elif action_index == '2':
            args_menu()
        elif action_index.lower() == 'exit':
            exit(1)
        else:
            main_menu()


single_text ='单线程下载（默认多线程下载）'
mul_text ='多线程下载'
all_text ='下载所有图片（默认最多只下载20套）'
not_all_text ='下载前20套图片'

thread_state = ['多线程','单线程']
pic_num_stat = ['部分','全部']

def args_menu():
    global multThread,all_result
    if multThread:state1 = thread_state[0]
    else:state1 = thread_state[1]
    if all_result:state2 = pic_num_stat[1]
    else:state2 = pic_num_stat[0]
    state_text = state1 +' '+ state2
    if multThread: thread_text = single_text
    else:thread_text=mul_text
    if all_result:pic_num_text = not_all_text
    else:pic_num_text=all_text
    view = '-'*25+' 设置 '+'-'*25 +\
           '\n 当前：' +state_text+' ' * (21-len(state_text)) + close_hint + \
           '\n 1 ' +thread_text+ \
           '\n 2 '+ pic_num_text+ \
           '\n 3 '+ '保存路径' + \
           '\n 4 返回上一级\n' \
            +'-'* (56)
    print(view + '\r')
    action_index = input('请选择一项： ')
    if len(action_index) == 0:
        args_menu()
    else:
        if action_index == '1':
            if multThread:
                multThread = False
            else:
                multThread = True
            args_menu()

        elif action_index == '2':
            if all_result:
                all_result = False
            else:
                all_result = True
            args_menu()

        elif action_index == '3':
            while True:
                path = input('请输入图片保存目录的路径:')
                if path.lower() == 'exit':
                    break
                if (not checkfile(path)[0]) or (checkfile(path)[0] == True and checkfile(path)[1] == 1):
                    print('您指定的路径不是文件夹,请重新输入')
                    continue
                else:
                    global save_path
                    save_path = path
                    args_menu()
                    break
            exit(1)
        elif action_index == '4':
            main_menu()

        elif action_index.lower() == 'exit':
            exit(1)
        else:
            args_menu()



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

    print_author_info('美女图片下载程序'+ '  ' +'数据源：'+base_url)

    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--keyword', required=False, help=('关键词'))
    parser.add_argument('-s', '--single_thread', required=False, help=('单线程'))
    parser.add_argument('-a', '--all', required=False, help=('下载所有图片'))
    parser.add_argument('-d', '--dir', required=False, help=('保存路径'))



    args = parser.parse_args()

    no_any_arg = True

    if args.all:
        no_any_arg = False
        all_result = True

    if args.single_thread:
        no_any_arg = False
        multThread = False

    if args.keyword :
        no_any_arg = False

    if args.dir :
        while True:
          if (not checkfile(args.dir)[0]) or (checkfile(args.dir)[0] == True and checkfile(args.dir)[1] == 1):
              args.dir = input('您指定的路径不是文件夹,请重新输入:')
          else:
              break
        save_path = args.dir
        no_any_arg = False

    if not no_any_arg:
        if not args.keyword:
            main_menu()
        else:
            searchMeinv(args.keyword)
    else:
        main_menu()




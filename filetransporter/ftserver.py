#!/usr/bin/env python
# -*- coding:utf-8 -*-
#。——————————————————————————————————————————
#。
#。  ftserver.py
#。
#。 @Time    : 2018/7/26 00:09
#。 @Author  : capton
#。 @Software: PyCharm
#。 @Blog    : http://ccapton.cn
#。 @Github  : https://github.com/ccapton
#。 @Email   : chenweibin1125@foxmail.com
#。__________________________________________
import sys,os
import socket
import threading
import argparse

from util import dir_divider,anti_dir_divider,judge_unit,checkfile,formated_time
import time

from language_words import languageSelecter

divider_arg  = ' _*_ ' # 指令内部的分隔符
right_arrows = '>'*10  # 输出占位符
left_arrows  = '<'*10  # 输出占位符

default_data_socket_port = 9997     # 默认的数据传输套接字端口号
default_command_socket_port = 9998  # 默认的指令传输套接字端口号

COMMAND_CLOSE = '[COMMAND CLOSE]'
COMMANE_MISSION_SIZE = '[COMMAND MISSION_SIZE]'

# socket封装类，用于简化socket输出编码的str内容的步骤
class Messenger:
    def __init__(self,socket):
        self.socket = socket
        self.send_debug = False
        self.recev_debug = False

    def send_msg(self,msg):
        if self.socket:
            try:
               self.socket.send(bytes(msg ,encoding='utf8'))
            except Exception as e:
                if self.send_debug:print(dict('ce'))
        elif self.send_debug:print(dict('sin'))
        return self

    def recv_msg(self):
        if self.socket:
            try:
                msg = self.socket.recv(1024)
                return bytes(msg).decode('utf8')
            except Exception as e:
                if self.recev_debug:print(dict('ce'))
        elif self.recev_debug:  print(dict('sin'))
        return None

# 指令线程类
class CommandThread(threading.Thread):
    def __init__(self, host=None, port=default_command_socket_port):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.working = True
        self.dataOn = True
        self.wait_client_flag = True
        self.mission_size = 0
        self.wrote_size = 0
        self.start_time = 0

    def setDataThread(self, server):
        self.dataThread = server

    def run(self):
        self.ssocket = socket.socket()
        self.ssocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.ssocket.bind((self.host, self.port))
            self.ssocket.listen(1)
            while self.wait_client_flag:
                socket2, addr = self.ssocket.accept()
                self.socket = socket2
                self.socket.send(
                    bytes(dict('ctcs') + self.host + ':' + str(self.port), encoding='utf8'))
                self.commandMessenger = Messenger(self.socket)
                command = self.commandMessenger.recv_msg()
                self.start_time = time.time()
                while command and len(command) and self.working> 0:
                    if command.startswith(COMMANE_MISSION_SIZE):
                        self.mission_size = int(command.split(divider_arg)[1])
                        print(dict('m_s')+': %.2f%s' % (
                        judge_unit(self.mission_size)[0], judge_unit(self.mission_size)[1]))
                    elif command == COMMAND_CLOSE:
                        self.dataOn = False
                        time.sleep(0.3)
                        Warning(right_arrows+dict('rcd')+left_arrows)
                    else:
                        self.fileMission = FileMission(self.dataThread.socket, self, self.dataThread.save_path, command)
                        self.fileMission.start()
                        self.dataOn = True
                    command = self.commandMessenger.recv_msg()
        except OSError:
            warning(dict('cara'))
            self.wait_client_flag = False

    # 告诉客户该文件已经准备好接受数据了
    def file_ready(self,fileinfo):
        self.commandMessenger.send_msg(fileinfo + divider_arg +'ready')

    # 告诉客户该文件已经传输完毕了
    def file_transportover(self,fileinfo):
        self.commandMessenger.send_msg(fileinfo + divider_arg +'file_transport_ok')

    # 告诉客户该文件夹已经创建好了
    def dir_created(self,fileinfo):
        self.commandMessenger.send_msg(fileinfo + divider_arg +'dir_create_ok')

    # 告诉客户根文件夹已经创建好了
    def rootdir_create(self,fileinfo):
        self.commandMessenger.send_msg(fileinfo + divider_arg +'rootdir_create_ok')

# 服务线程类 ，在此处理数据套接字，并 和指令线程类CommandThread相互调用完成传输任务
class Server(threading.Thread):
    def __init__(self,save_path,host = None,port = 9997):
        threading.Thread.__init__(self)
        self.save_path = save_path
        self.host = host
        self.port = int(port)
        self.wait_client_flag = True
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path) # 若文件保存的根目录不存在，则创建它
        print(dict('fsd') + self.save_path)

    # 设置指令线程实例
    def setCommandThread(self,commandThread):
        self.commandThread = commandThread

    def run(self):
        self.start_server_socket()
        self.wait_client()

    # 开启socket监听
    def start_server_socket(self):
        self.ssocket = socket.socket()
        self.ssocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.ssocket.bind((self.host, self.port))
            print(dict('shs'))
            print(dict('ra')+' (%s,%d)' % (self.host, self.port))
            print(dict('wfft')+'...')
        except OSError:
            self.wait_client_flag = False
            pass

    # 阻塞线程 循环接收新的客户端数据套接字连接
    def wait_client(self):
        self.ssocket.listen(5)  # 等待客户端连接
        while self.wait_client_flag:
            socket, addr = self.ssocket.accept()  # 建立客户端连接。
            print(dict('nc'), addr)
            try:
                socket.send(bytes(dict('ctds') + self.host + ':' + str(self.port), encoding="utf8"))
                self.socket = socket
                self.commandThread.setDataThread(self)
                self.commandThread.dataOn = True
            except ConnectionResetError as e:
                print(dict('aoc')+'\n')
                print(dict('wfft')+'...')

# 任务线程类，复制文件的下载，并和数据线程类Server、指令线程类CommandThread通信
class FileMission(threading.Thread):
    def __init__(self,socket,commandThread,save_path,fileinfo):
        threading.Thread.__init__(self)
        self.commandThread = commandThread
        self.socket = socket
        self.save_path = save_path
        self.fileinfo = fileinfo
        self.working = True

    def run(self):
        self.handleMission()

     # 分析客户端传过来的文件信息（若是文件夹，则新建文件夹；若是文件，则准备从套接字socket对象中读取数据写入新文件中）
    def handleMission(self):
        if self.fileinfo:  # 解析fileinfo文本，分析出文件夹、文件信息
            self.filename = self.fileinfo.split(divider_arg)[0]
            self.filename = self.filename.replace(anti_dir_divider(), dir_divider())
            self.file_path = str(self.save_path + dir_divider() + self.filename)
            self.file_path = self.file_path.replace(anti_dir_divider(), dir_divider())
            self.filesize = int(self.fileinfo.split(divider_arg)[1])
        if self.filesize > 0: # 若是文件，则用套接字发送指令通知客户端已准备接收数据
            self.commandThread.file_ready(self.fileinfo)
            self.write_filedata(self.fileinfo)
        else:                 # 若是文件夹，则在本地创建文件夹并童套接字通知客户端已创建完文件夹了
            if not os.path.exists(self.file_path):
                os.makedirs(self.file_path)
            index = int(self.fileinfo.split(divider_arg)[2])
            dir = self.fileinfo.split(divider_arg)[0]

            if index == 0:
                print(right_arrows+dict('ms')+left_arrows)
                print('-' * 30)
                self.commandThread.rootdir_create(self.fileinfo)
            else:
                self.commandThread.dir_created(self.fileinfo)
            print(dict('cd')+': ' + dir)

     # 读取socket原始数据，写入文件中
    def write_filedata(self,fileinfo):
        print(dict('st')+'%s %.2f%s' % (self.filename,judge_unit(self.filesize)[0],judge_unit(self.filesize)[1]))
        with open(self.file_path,'wb') as f:
            wrote_size = 0
            filedata = self.socket.recv(1024)
            while len(filedata) > 0 :
                tempsize = f.write(filedata)
                wrote_size += tempsize
                self.commandThread.wrote_size += tempsize
                f.flush()
                downloaded_show = '%.2f%s/%.2f%s' % (judge_unit(wrote_size)[0], judge_unit(wrote_size)[1],
                                                     judge_unit(self.filesize)[0], judge_unit(self.filesize)[1])
                total_downloaded_show = '%.2f%s/%.2f%s' % (judge_unit(self.commandThread.wrote_size)[0],
                                                           judge_unit(self.commandThread.wrote_size)[1],
                                                     judge_unit(self.commandThread.mission_size)[0],
                                                           judge_unit(self.commandThread.mission_size)[1])
                current_filename = os.path.basename(self.filename) +' '
                sys.stdout.write(current_filename+downloaded_show +' | %.2f%%  >>>%s %s | %.2f%%' %
                                 (float(wrote_size / self.filesize * 100),
                                  dict('total'),
                                  total_downloaded_show,
                                  float(self.commandThread.wrote_size / self.commandThread.mission_size * 100))+ '\r')
                if wrote_size == self.filesize:
                    print()
                    print(self.filename + ' ' + dict('dd'))
                    self.commandThread.file_transportover(self.fileinfo)
                    if not self.commandThread.dataOn:
                        self.socket.close()
                    break
                else:
                    try:
                        filedata = self.socket.recv(1024)
                    except ConnectionResetError:
                        warning(right_arrows+ dict('rcd')+left_arrows)

            if wrote_size < self.filesize:
                warning(right_arrows+dict('ci')+left_arrows)
                self.dataOn = False
                self.socket.close()
                self.commandThread.socket.close()
                self.commandThread.wrote_size = 0
                self.commandThread.mission_size = 0

            print('-'*30)
            if self.commandThread.wrote_size == self.commandThread.mission_size and self.commandThread.wrote_size != 0:
                self.commandThread.wrote_size = 0
                self.commandThread.mission_size = 0
                print(right_arrows+dict('mc')+left_arrows)
                print(dict('cmct')+'%s' % formated_time(time.time() - self.commandThread.start_time))
                print(dict('ra')+' (%s,%d)' % (self.commandThread.dataThread.host, self.commandThread.dataThread.port))
                print(dict('wfft')+'...')

def warning(text):
    print('[%s] '% dict('wa')+text)

def keyInPort():
    while True:
        temp_port = input(dict('ip'))
        if int(temp_port) > 0 and int(temp_port) != default_command_socket_port:
            return (int(temp_port),True)
        elif int(temp_port) <= 0:
            warning(dict('pmb'))
        elif int(temp_port) == default_command_socket_port:
            warning('Port %d is disabled,please key in other number' % default_command_socket_port)


def keyInSavePath():
    while True:
        filepath = input(dict('pidp'))
        if checkfile(filepath)[0] and checkfile(filepath)[1] == 0:
            return filepath, True
        elif not checkfile(filepath)[0]:
            warning(dict('pde'))
        elif checkfile(filepath)[0] and checkfile(filepath)[1] == 1:
            warning(dict('dpif'))


def keyInHost():
    while True:
        host = input(dict('pit'))
        if len(host) > 0:
            return host, True

def print_author_info(program_name):
    print('*'*60)
    line = 9
    while line > 0:
      if line == 8:
          print('。  %s' % program_name)
      elif line == 6:
          print('。  @ %s: Capton' % dict('Author'))
      elif line == 5:
          print('。  @ %s: http://ccapton.cn' % dict('Blog'))
      elif line == 4:
          print('。  @ %s: chenweibin1125@foxmail.com' % dict('Email'))
      elif line == 3:
          print('。  @ %s: https://github.com/ccapton' % dict('Github'))
      elif line == 2:
          print('。  @ %s: https://github.com/Ccapton/python-stuff/tree/master/filetransporter' % dict('Project'))
      else:
          print('。')
      line -= 1
    print('*'*60)

def dict(key):
    return languageSelecter.dict(key)

if __name__ == '__main__':

    print_author_info(dict('ftsp'))
    #if len(sys.argv) == 1:
    #    sys.argv.append('--help')

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', required=False, help=(dict('tdpw')))
    parser.add_argument('-p', '--port', required=False, help=(dict('tptp')) ,type = int)
    parser.add_argument('-i', '--host', required=False, help=(dict('thtp')),type = str)

    args = parser.parse_args()


    port = default_data_socket_port
    port_ok = True
    host_ok = False
    save_path_ok = False

    save_path = args.dir
    if not save_path:
        save_path = 'downloads'
        if checkfile(save_path)[0] and checkfile(save_path)[1] == 0:
            if not os.path.exists(save_path):os.makedirs(save_path)
        save_path_ok = True
    else:
        if not checkfile(save_path)[0]:
            warning(dict('pde'))
            save_path,save_path_ok = keyInSavePath()
        else:
            save_path_ok = True

    if args.host:
        host = args.host
        host_ok = True
    else:
        myname = socket.getfqdn(socket.gethostname())
        host = socket.gethostbyname(myname)
        host_ok = True

    if args.port and args.port > 0 :
        port = args.port
        if port == default_command_socket_port:
            warning(dict('po')+' %d %s,%s' % (dict('id'),dict('pki'),default_command_socket_port))
            port , port_ok = keyInPort()
    elif args.port and args.port <=0:
        warning(dict('pmb'))
        port, port_ok = keyInPort()

    if port_ok and host_ok and save_path_ok:
        commandThread = CommandThread(host=host)
        server = Server(save_path=save_path,host = host, port=port)
        server.setCommandThread(commandThread)
        server.start()
        commandThread.setDataThread(server)
        commandThread.start()


#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2018/7/24 14:09
# @Author  : capton
# @FileName: ftclient.py
# @Software: PyCharm
# @Blog    : http://ccapton.cn
# @Github  : https://github.com/ccapton
# @Email   : chenweibin1125@foxmail.com

import sys
import socket
import threading
import argparse

from list_file import *
from util import judge_unit,relative_path,dir_divider,checkfile


divider_arg =  ' _*_ '

msg_index = 0

isCommandTConnected= False

default_data_socket_port = 9997
default_command_socket_port = 9998

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
                if self.send_debug:print('connect error')
        elif self.send_debug:print('socket is none')
        return self

    def recv_msg(self):
        if self.socket:
            try:
                msg = self.socket.recv(1024)
                return bytes(msg).decode('utf8')
            except Exception as e:
                if self.recev_debug:print('connect error')
        elif self.recev_debug:  print('socket is none')
        return None

class CommandThread(threading.Thread):
    def __init__(self, host=None, port=default_command_socket_port):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.working = True
        self.messanger = None

    def setMissionSize(self,mission_size):
        self.mission_size = mission_size

    def setDataThread(self, server):
        self.dataThread = server

    def run(self):
        self.socket = socket.socket()
        try:
            self.socket.connect((self.host, self.port))
            global isCommandTConnected
            isCommandTConnected = True
            self.messanger = Messenger(self.socket)
            try:
                command = bytes(self.socket.recv(1024)).decode(encoding='utf8')
                if self.working:
                   print(command)
                self.messanger.send_msg('mission_size' + divider_arg + str(self.mission_size))
                while self.working and command and len(command) > 0:
                    if command.endswith('rootdir_create_ok'):
                        self.dataThread.waitingCreateDir = False
                    elif command.endswith('file_transport_ok') or command.endswith('dir_create_ok'):
                        self.dataThread.filefinder.recycle = False
                    elif command.endswith('ready'):
                        self.dataThread.send_filedata()
                    command = self.messanger.recv_msg()
                    if not self.working:
                        if sumsize == self.dataThread.sumsize:
                            print('>>>>>>>>>>Mission Complished!<<<<<<<<<')
                        self.socket.close()
            except ConnectionResetError as e:
                self.working = False
                if self.dataThread.filefinder:
                    self.dataThread.filefinder.finderCallback = None
                    self.dataThread.filefinder.recycle = True
                    self.dataThread.filefinder.off = True
                self.socket.close()
                self.dataThread.socket.close()
                print('>>>>>>>Connection Interrupted<<<<<<<')
                print(' Please Try The Mission Once Againg...')
            except OSError as e:
                print('No route to host(%s)' % self.host)

        except Exception:
            print('>>>>>>>Connect Error<<<<<<<')



    def send_fileinfo(self,fileinfo):
        if self.messanger:
            self.messanger.send_msg(fileinfo)

    def send_command(self,msg):
        if self.messanger:
            self.messanger.send_msg(msg)


class Client(threading.Thread , FileFinder.FinderCallback):
    def __init__(self,host,port):
        threading.Thread.__init__(self)
        self.filefinder = None
        self.host = host
        self.port = port
        self.singFile = True
        self.findfileOver = False
        self.sumsize = 0
        self.mission_read_size = 0
        self.waitingCreateDir = True
        self.once = True

    def setCommandThread(self, commandThread):
        self.commandThread = commandThread

    def setFilePath(self,filepath):
        self.filepath = filepath
        self.rootpath = filepath

    def onFindDir(self,dir_path):
        global msg_index
        msg_index += 1
        print('Creating Dir '+ os.path.basename(self.rootpath)+dir_divider()+relative_path(self.rootpath,dir_path))
        self.filename = dir_path
        self.filesize = -1
        self.commandThread.send_fileinfo(os.path.basename(self.rootpath) + dir_divider()
                                               +relative_path(self.rootpath,dir_path)+ divider_arg
                                               +str(-1)+divider_arg+str(msg_index))

    def onFindFile(self,file_path,size):
        global msg_index
        msg_index += 1
        self.sumsize += size
        print('Transporting File '+ os.path.basename(self.rootpath)+dir_divider()+relative_path(self.rootpath,file_path) +
              ' '+ '%.2f%s' % (judge_unit(size)[0],judge_unit(size)[1]))
        self.filename = file_path
        self.filesize = size
        if (os.path.isfile(file_path) and relative_path(self.rootpath,file_path) == ''):
            self.commandThread.send_fileinfo(os.path.basename(file_path) + divider_arg + str(size)+divider_arg+str(msg_index))
        else:
            self.commandThread.send_fileinfo(os.path.basename(self.rootpath)+ dir_divider()
                                               +relative_path(self.rootpath,file_path)+ divider_arg +str(size)
                                                   + divider_arg + str(msg_index))

    def run(self):

        if checkfile(self.filepath)[0] and checkfile(self.filepath)[1] == 1:
            self.singFile = True
            if self.connect_to_server():
                self.filefinder = FileFinder(self)
                self.filefinder.recycle = False
                self.filefinder.list_flie(self.filepath)
        elif checkfile(self.filepath)[0] and checkfile(self.filepath)[1] == 0:
            self.singFile = False
            self.findfileOver = False
            if self.connect_to_server():
                print('Creating Dir ' + os.path.basename(self.filepath))
                self.commandThread.send_command(os.path.basename(self.filepath) + divider_arg +'-1' +divider_arg + str(msg_index))
                while self.waitingCreateDir:
                    time.sleep(0.1)
                self.waitingCreateDir = True
                self.filefinder = FileFinder(self)
                self.filefinder.recycle = False
                self.filefinder.list_flie(self.filepath)
                self.findfileOver = True

        elif not checkfile(self.filepath)[0]:
            print('Please input correct file path')

    def connect_to_server(self):
        self.socket = socket.socket()
        try:
            self.socket.connect((self.host, self.port))
            print(bytes(self.socket.recv(1024)).decode(encoding='utf8'))
            print('Mission Start!')
            print('-'*30)
            return True
        except ConnectionError as e:
            if isCommandTConnected:
                print('The Server Is Working,But Data Socket Is Not Working On Port %d' % self.port)
                print('>>>>>>>Connection Disconnected<<<<<<<')
                self.commandThread.messanger.send_msg('[COMMAND CLOSE]')
                self.commandThread.socket.close()
                self.commandThread.working = False
            else:
                print('>>>>>>>Connect error<<<<<<<'
                  ' \n Please Confirm The Server Is Working Well? \n Or Check The Server\'s Address Is The Same As The Parameters You Key In\n '+
                  'The Host And Port You Key In Is ( %s , %d )' % (self.host,self.port))
        except OSError as e:
            print('No route to host(%s)' % self.host)
        return False


    def send_filedata(self):
        readed_size = 0
        with open(self.filename,'rb') as f:
            filedata = f.read(1024)
            while len(filedata) > 0 :
                tempsize = len(filedata)
                readed_size += tempsize
                self.mission_read_size += tempsize
                try:
                   self.socket.send(filedata)
                   readed_show = '%.2f%s/%.2f%s' % (judge_unit(readed_size)[0], judge_unit(readed_size)[1],
                                                    judge_unit(self.filesize)[0], judge_unit(self.filesize)[1])
                   total_readed_show = '%.2f%s/%.2f%s' % (judge_unit(self.mission_read_size)[0],
                                                          judge_unit(self.mission_read_size)[1],
                                                          judge_unit(sumsize)[0],
                                                          judge_unit(sumsize)[1])
                   current_filename = os.path.basename(self.filename) + ' '
                   sys.stdout.write(current_filename + readed_show + ' | %.2f%%  >>>Total %s | %.2f%%' %
                                    (float(readed_size / self.filesize * 100),
                                     total_readed_show,
                                     float(self.mission_read_size / sumsize * 100)) + '\r')
                except BrokenPipeError as e:
                    if self.once:
                        if self.filefinder:
                            self.filefinder.finderCallback = None
                            self.filefinder.recycle = True
                            self.filefinder.off = True
                        print('>>>>>>>Remote Conenction Destoried<<<<<<<')
                        self.once = False

                filedata = f.read(1024)
        print()
        if  readed_size == self.filesize and readed_size == 0:
            print(os.path.basename(self.filename) + ' finished')
        print('—'*30)
        if self.singFile:
            self.commandThread.send_command('[COMMAND CLOSE]')
            self.socket.close()
            self.commandThread.working = False
        else:
            if self.findfileOver:
                self.commandThread.send_command('[COMMAND CLOSE]')
                self.socket.close()
                self.commandThread.working = False

class MyfinderCallback(FileFinder_Fast.FinderCallback):
    def __init__(self):
        self.sumsize = 0
    def onFindDir(self,dir_path):
        pass
    def onFindFile(self,file_path,size):
        self.sumsize += size


def keyInPort():
    while True:
        temp_port = input('Input Port : ')
        if int(temp_port) > 0 and int(temp_port) != default_command_socket_port:
            return (int(temp_port),True)
        elif int(temp_port) <= 0:
            warning('Port Must Be Positive Number!')
        elif int(temp_port) == default_command_socket_port:
            warning('Port %d is disabled,please key in other number' % default_command_socket_port)


def keyInFilePath():
    while True:
        filepath = input('Please Input File Or Dir Path:')
        if filepath.endswith(dir_divider()):
            filepath2 = filepath[:len(filepath)-1]
        else:
            filepath2 = filepath
        if checkfile(filepath2)[0]:
            return filepath2, True
        else:
            print('Path Doesn\'t Exist!')

def keyInHost():
    while True:
        host = input('Please Input The Target Host:')
        if len(host) > 0:
            return host, True


def print_author_info(program_name):
    print('*'*60)
    line = 9
    while line > 0:
      if line == 8:
          print('.  %s' % program_name)
      elif line == 6:
          print('.  @ Author: %s' % 'Capton')
      elif line == 5:
          print('.  @ Blog: %s' % 'http://ccapton.cn')
      elif line == 4:
          print('.  @ Email: %s' % 'chenweibin1125@foxmail.com')
      elif line == 3:
          print('.  @ Github: %s' % 'https://github.com/ccapton')
      elif line == 2:
          print('.  @ Project: %s' % 'https://github.com/ccapton/python-stuff/filetransport')
      else:
          print('.')
      line -= 1
    print('*'*60)

def warning(text):
    print('[Warning] '+text)

if __name__ == '__main__':
    # python ft_client -f /Users/capton/desktop/test.mp4 -h 127.0.0.1 -p 5050'

    # if len(sys.argv) == 1:
    #    sys.argv.append('--help')
    print_author_info('FileTransporter Client Program')

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filepath', required=False, help=('the path which file will send'))
    parser.add_argument('-p', '--port', required=False, help=('the port that program data will transport'),type = int)
    parser.add_argument('-i', '--host', required=False, help=('the hostip that program data will transport to'),type = str)

    args = parser.parse_args()

    port = default_data_socket_port

    filepath_ok = True
    port_ok = True
    host_ok = False
    if args.port and args.port > 0 :
        port = args.port
        if port == default_command_socket_port:
            warning('Port %d is disabled,please key in other number' % default_command_socket_port)
            port , port_ok = keyInPort()
    elif args.port and args.port <=0:
        warning('Port Must Be Positive Number!')
        port, port_ok = keyInPort()

    filepath = args.filepath
    if not filepath:
        filepath , filepath_ok = keyInFilePath()
    elif not checkfile(args.filepath)[0]:
        warning('Path Doesn\'t Exist！')
        filepath , filepath_ok = keyInFilePath()

    host = args.host
    if not host:
        host , host_ok = keyInHost()
    else:
        host_ok = True

    if port_ok and filepath_ok and host_ok:
        findercallback = MyfinderCallback()
        if not checkfile(filepath)[1]:
           print('Finding Files In %s...' % filepath)
        FileFinder_Fast(findercallback).list_flie(filepath)
        global sumsize
        sumsize = findercallback.sumsize
        file_type = ''
        if checkfile(filepath)[1]:
            file_type = 'The File :'
        else:
            file_type = 'The Dir (And All Files In This Dir):'
        warning('You Are Going To Transport %s' % file_type)
        print(filepath + ' | Totoal Size : %.2f%s' % (judge_unit(sumsize)[0],judge_unit(sumsize)[1]))

        confirm = input('Continue To Transport? (Y/N):')
        while True:
            if confirm == 'y' or confirm == 'Y' or confirm == 'Yes'.upper() or confirm == 'yes'.lower():
                client = Client(host, port)
                commandThread = CommandThread(host)
                commandThread.setDataThread(client)
                commandThread.setMissionSize(sumsize)
                client.setCommandThread(commandThread)
                client.setFilePath(filepath)
                client.start()
                commandThread.start()
                break
            elif confirm == 'n' or confirm == 'N' or confirm == 'No'.upper() or confirm == 'no'.lower():
                warning('Give Up Mission...Continue')
                break
            confirm = input('Continue To Transport? (Y/N):')


# 岛国裡蕃爬虫、及其数据api输出服务
### 代码下载
https://github.com/Ccapton/python-stuff/releases/download/lifan_1.1/lifan.zip

### 数据成果展示
根据爬取的数据自制[接口api](http://ccapton.fun/lifan) 

### 安装必备包
```python
pip3 install -r requirements.txt
```

### 爬虫部分
请详细阅读spider.py、models.py、stc.py等文件源码
然后运行spider.py
```python
python3 spider.py -auto 666
```
### 如何配置api服务器
请阅读**constant.py**这个文件内容
你会发现
```python

'''
若你的vps只有一个公网ip，则ip,publicIP都设置为这一个公网ip值
若有公网ip和内网ip则，开启web服务器时用内网ip
'''
ip = '10.135.120.137'         # vps虚拟云主机内网ip
publicIP = '111.230.231.107'  # vps虚拟云主机公网ip
localIp = '0.0.0.0'           # 本地公共ip，供局域网内用户访问

psw = 666                     # 误操作密码
port = 5050                   # 接口服务器端口号

"""
  设置当前ip ，若开发环境，则 currentIp = localIp，否则 currentIp = publicIP
"""
# currentIp = publicIP        # 当前ip设置为公网ip
currentIp = localIp           # 当前ip设置为本地ip
```
### 应用场景
1、 用在**测试环境**下，运行**lifan-debug.py**
```python
python3 lifan-debug.py
```

2、用在**正式环境**下，请先到 **constant.py** 修改  内网ip、公网publicIp,以及设置:
currentIp = publicIP 。

然后运行
```python
python3 lifan.py
```
反之，转到测试环境下，则是 currentIp = localIp

### 注意事项
因为现在的数据库已经保存了以本地ip '0.0.0.0' 作为图片服务器地址了，所以当要在工作的服务器上直接使用已有数据的话，请
先到**constant.py**修改 公网publicIp、内网ip 以及设置 currentIp = publicIP 后 再运行
```python
python3 spider.py -update <任意字符>
```

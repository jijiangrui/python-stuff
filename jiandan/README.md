# 煎蛋网女生图片爬虫

### 下载必要文件 PhantomJS
文件下载地址 http://phantomjs.org/download.html，放置本文件jiandan.py同目录下
### 安装环境
```python
pip3 install -r requirements.txt
```
### 执行
```python
python3 jiandan.py 
```
执行后输入图片保存目录的路径
### 说明
这个爬虫严格意义上已经不配叫爬虫了，它很慢，毕竟目标网站的img指向地址是js动态生成的，这里用浏览器模拟器访问得到关键的图片地址。

有时模拟器会访问网页失败，或者图片下载失败，请重试几次就好了。
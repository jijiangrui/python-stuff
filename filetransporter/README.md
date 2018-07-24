# FileTransporter

###这是一个基于socket的文件（夹）传输程序

#### ftserver.py ：**接收端程序**
 
 * **基本用法**
```python
python3 ftserver.py 
```
默认主机地址：计算机本地ip （例如 '192.168.1.100'）,  默认下载目录： downloads

* **详细用法**  （带参数）
```html
-i 设置主机名称（地址）

-p 指定端口号

-d 指定文件（夹）保存路径
```
**示例**

先用 cd 命令 切换到 ftserver.py 所在文件夹，然后：
```python
python3 ftserver.py -i 192.168.1.100 -p 9909 -d /users/Capton/desktop
```
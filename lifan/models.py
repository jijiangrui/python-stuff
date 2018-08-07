#coding=utf-8
#。—————————————————————————————————————————— 
#。                                           
#。  models.py 模型类
#。                                           
#。 @Time    : 2018/8/3 15:10                
#。 @Author  : capton                        
#。 @Software: PyCharm                
#。 @Blog    : http://ccapton.cn              
#。 @Github  : https://github.com/ccapton     
#。 @Email   : chenweibin1125@foxmail.com     
#。__________________________________________

'''
双裡蕃表，设计初衷：
所有图片总大小不超过500Mb,本地服务器完全可以保存，不需要第三方服务器托管
所以就有下载图片的过程，而如果只用一张表保存图片地址，考虑到图片下载会失败的问题，容易混淆图片的最终地址
'''

from peewee import *
from constant import db_save_path
import os

if not os.path.exists(db_save_path):
    os.makedirs(db_save_path)

db = SqliteDatabase(os.path.join(db_save_path,'lifan_database.db'))

class BaseModel(Model):
    class Meta:
        database = db

# 目录类
class Category(BaseModel):
    index = IntegerField()
    name = CharField()
    def __str__(self):
        return self.__class__.__name__ + ' %s %s' % (self.index,self.name)

# 服务端 Lifan 类， 用于保存爬取的数据
class LifanS(BaseModel):
    category = CharField() # 目录名
    title = CharField()    # 标题
    magnet = CharField()   # 磁力链
    cover_s = CharField()  # 小封面地址 （存入原始图片地址）
    cover_l = CharField()  # 大封面地址 （存入原始图片地址）
    index = IntegerField() # 序号（查找时排序的依据属性）
    def __str__(self):
        return self.__class__.__name__ + ' %s %s %s %s %s %s' % (self.index,self.category,self.title,self.magnet,
                                                                 self.cover_s,self.cover_l)

# 客户端 Lifan 类， 修改图片地址后，用于对外提供数据
class LifanC(BaseModel):
    category = CharField() # 目录名
    title = CharField()    # 标题
    magnet = CharField()   # 磁力链
    cover_s = CharField()  # 小封面地址 （存入对外公布的图片网络地址，此时图片要下载到本服务器内）
    cover_l = CharField()  # 大封面地址 （存入对外公布的图片网络地址，此时图片要下载到本服务器内）
    index = IntegerField() # 序号（查找时排序的依据属性）
    def __str__(self):
        return self.__class__.__name__ + ' %s %s %s %s %s %s' % (self.index,self.category,self.title,self.magnet,
                                                                 self.cover_s,self.cover_l)

db.connect()
db.create_tables([LifanS,LifanC, Category])


#coding=utf-8
#。—————————————————————————————————————————— 
#。                                           
#。  models.py                               
#。                                           
#。 @Time    : 2018/8/8 23:23                
#。 @Author  : capton                        
#。 @Software: PyCharm                
#。 @Blog    : http://ccapton.cn              
#。 @Github  : https://github.com/ccapton     
#。 @Email   : chenweibin1125@foxmail.com     
#。__________________________________________


from peewee import *
from constants import db_save_path
import os

if not os.path.exists(db_save_path):
    os.makedirs(db_save_path)

db = SqliteDatabase(os.path.join(db_save_path,'iqiyi_database.db'))

class BaseModel(Model):
    class Meta:
        database = db

class IqiyiVmovieModel(BaseModel):
    name = CharField()
    img_url = CharField()
    area = CharField()
    movie_type = CharField()
    movie_standard = CharField()
    generation = CharField()
    actors = CharField()
    html_url = CharField()
    url_type = IntegerField()
    url = CharField()
    update_time = DateTimeField()
    def __str__(self):
        return self.__class__.__name__ + ' %s %s %s %s %s %s %s %s %s %s %s' %\
               (self.name,self.img_url,self.area,self.movie_type,self.movie_standard,self.generation,
                self.actors,self.html_url,self.url_type,self.url,self.update_time)


db.connect()
db.create_tables([IqiyiVmovieModel])

#coding=utf-8
#。—————————————————————————————————————————— 
#。                                           
#。  lifan-api.py
#。                                           
#。 @Time    : 2018/8/4 23:10                
#。 @Author  : capton                        
#。 @Software: PyCharm                
#。 @Blog    : http://ccapton.cn              
#。 @Github  : https://github.com/ccapton     
#。 @Email   : chenweibin1125@foxmail.com     
#。__________________________________________

from flask_restful import Resource,reqparse
from util import showResult

from db.data_transformer import *


# Resource封装类，简化数据参数的配置
class BaseResource(Resource):
    def __init__(self):
        Resource.__init__(self)
        self.parser = reqparse.RequestParser()
        self.add_args()
        self.create_args()

    # 等待子类重写
    def add_args(self):
        pass

    def add_argument(self, *args, **kwargs):
        self.parser.add_argument(*args, **kwargs)

    def create_args(self):
        self.args = self.parser.parse_args()

    def get_arg(self, key):
        return self.args[key]


'''
 code 
 0 正常
 1 category 错误 
'''

class LifanResource(BaseResource):
    def add_args(self):
        self.add_argument('index',type=int,help='category index')
        self.add_argument('page',type=int,help='lifan data show in pages')
        self.add_argument('size',type=int,help='size of each page')

    def get(self):
        if self.get_arg('index') == None:
            return showResult(0, 'show categories successful', dict_categories())
        elif self.get_arg('index') == 0:
            return showResult(0,'show categories successful',dict_categories())
        else:
            for category in get_categories():
                if self.get_arg('index') ==  category.index:
                   return showResult(0,'show lifans successful',
                                     get_lifan_by_category(category.index,
                                                           category.name,
                                                           self.get_arg('page'),
                                                           self.get_arg('size')))
            return showResult(1,'category out of range')








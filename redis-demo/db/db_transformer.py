#coding=utf-8
#。—————————————————————————————————————————— 
#。                                           
#。  db_transformer.py                               
#。                                           
#。 @Time    : 2018/8/9 12:59                
#。 @Author  : capton                        
#。 @Software: PyCharm                
#。 @Blog    : http://ccapton.cn              
#。 @Github  : https://github.com/ccapton     
#。 @Email   : chenweibin1125@foxmail.com     
#。__________________________________________

from db.db_executor import *

def get_aqiyi_moviemodels_by_area(area,page,size,all=False):
    return DbExecutor().query_aqiyiVmovieModel_by_area(area.encode(encoding='utf-8').decode(encoding='utf-8'),page,size,all)


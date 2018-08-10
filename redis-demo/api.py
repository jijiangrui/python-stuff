#coding=utf-8
#。—————————————————————————————————————————— 
#。                                           
#。  api.py                               
#。                                           
#。 @Time    : 2018/8/9 13:22                
#。 @Author  : capton                        
#。 @Software: PyCharm                
#。 @Blog    : http://ccapton.cn              
#。 @Github  : https://github.com/ccapton     
#。 @Email   : chenweibin1125@foxmail.com     
#。__________________________________________

from db.db_transformer import get_aqiyi_moviemodels_by_area

if __name__ == '__main__':
    from constants import iqiayi_constants
    model_list = get_aqiyi_moviemodels_by_area(iqiayi_constants.get('areas')[3][1],2,40)
    print(len(model_list))
    for model in model_list:
        print(model)
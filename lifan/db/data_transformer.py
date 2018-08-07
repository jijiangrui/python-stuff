#coding=utf-8
#。—————————————————————————————————————————— 
#。                                           
#。  data_transformer.py
#。                                           
#。 @Time    : 2018/8/4 23:38                
#。 @Author  : capton                        
#。 @Software: PyCharm                
#。 @Blog    : http://ccapton.cn              
#。 @Github  : https://github.com/ccapton     
#。 @Email   : chenweibin1125@foxmail.com     
#。__________________________________________

from db.db_executor import CategoryExecutor,ClientLifanExecutor
from constant import category_url,currentIp,port

def get_categories():
    return CategoryExecutor().get_all_category()

def dict_categories():
    categories = CategoryExecutor().get_all_category()
    category_list = []
    for category in categories:
        index = category.index
        name = category.name
        category_list.append({'index':index,'name':name})
    return {'base_url':'http://'+currentIp+':'+str(port)+'/lifan/api',
            'useage-exp':u'示例请求地址：'+'http://'+currentIp+u':'+str(port)+'/lifan/api?index=999',
            'categories':category_list}

def get_lifan_by_category(index,category_name,page,size):
    lifan_list = []
    if page == None:
        page = 1
    if size == None:
        size = 20
    lifans =  ClientLifanExecutor().query_lifanC_by_category(category_name,page,size)
    for lifan in lifans:
        lifan_list.append({'title':lifan.title,
                           'magnet':lifan.magnet,
                           'category':lifan.category,
                           'cover_s':lifan.cover_s,
                           'cover_l':lifan.cover_l,
                           'index':lifan.index,})
    return {'category':category_name,'index':index,'lifans':lifan_list}

def get_lifan_by_category_index(index,page,size,all=True):
    for category in get_categories():
        if category.index == index:
            lifan_list = []
            if page == None:
                page = 1
            if size == None:
                size = 20
            lifans = ClientLifanExecutor().query_lifanC_by_category(category.name, page, size,all)
            for lifan in lifans:
                lifan_list.append({'title': lifan.title,
                                   'magnet': lifan.magnet,
                                   'category': lifan.category,
                                   'cover_s': lifan.cover_s,
                                   'cover_l': lifan.cover_l,
                                   'index': lifan.index, })
            return {'category': category.name, 'index': index, 'lifans': lifan_list}

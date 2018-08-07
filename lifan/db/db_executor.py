#coding=utf-8
#。—————————————————————————————————————————— 
#。                                           
#。  db_executor.py 数据库操作类
#。                                           
#。 @Time    : 2018/8/3 16:54                
#。 @Author  : capton                        
#。 @Software: PyCharm                
#。 @Blog    : http://ccapton.cn              
#。 @Github  : https://github.com/ccapton     
#。 @Email   : chenweibin1125@foxmail.com     
#。__________________________________________
from models import *

# 数据库操作基类
class DbExecutor:

    def __init__(self):
        self.open_db(1)
        self.open_db(2)

    def open_db(self,index):
        if index == 1:
           if db.is_closed():
               db.connect()
        if index == 2:
           pass

    def close_Db(self,index):
        if index == 1:
            if not db.is_closed():
                db.close()
        if index == 2:
            pass

    # 删除同一目录下的所有裡蕃
    def _delete_lifan_by_category(self,executor,category):
        try:
            if isinstance(executor,ClientLifanExecutor):
                lifan_list = LifanC.select().order_by(LifanC.index).where(LifanC.category == category)
                for lifan in lifan_list:
                    LifanC.delete().where(LifanC.category == lifan.category).execute()
                return True
            else:
                lifan_list = LifanS.select().order_by(LifanS.index).where(LifanS.category == category)
                for lifan in lifan_list:
                    lifan.delete().where(LifanS.category == lifan.category).execute()
                return True
        except:
            return False

    # 删除指定标题的裡蕃
    def _delete_lifan_by_title(self,executor,title):
        try:
            if isinstance(executor,ClientLifanExecutor):
                lifan_list = LifanC.select().order_by(LifanC.index).where(LifanC.title == title)
                for lifan in lifan_list:
                    lifan.delete()
                return True
            else:
                lifan_list = LifanS.select().order_by(LifanS.index).where(LifanS.title == title)
                for lifan in lifan_list:
                    lifan.delete()
                return True
        except:
            return False

    # 删除指定序号的目录
    def _delete_category_by_index(self,index):
        try:
            res = Category.get(Category.index == index)
        except DoesNotExist:
            res = None
        if res:
            try:
                res.delete()
                return True
            except:
                return False

    # 保存目录（无则插入，有则更新）
    # 返回元祖（数据库操作是否成功，操作类型：0 插入，1 更新）
    def _save_category(self,category):
        try:
            res = Category.get(Category.index == category.index)
        except DoesNotExist:
            res = None
        if res:
            try:
                res.index = category.index
                res.name = category.name
                res.save()
                return True, 1
            except:
                return False, 1
        else:
            try:
                category.save()
                return True, 0
            except:
                return False, 0

    # 保存裡蕃 （无则插入，有则更新）
    # 返回元祖（数据库操作是否成功，操作类型：0 插入，1 更新）
    def _save_lifan(self, lifan):
        if isinstance(lifan,LifanC):
            try:
                lifan_res = LifanC.get(LifanC.title == lifan.title)
            except DoesNotExist:
                lifan_res = None
        else:
            try:
                lifan_res = LifanS.get(LifanS.title == lifan.title)
            except DoesNotExist:
                lifan_res = None
        if lifan_res:
            try:
                lifan_res.cover_s = lifan.cover_s
                lifan_res.cover_l = lifan.cover_l
                lifan_res.title = lifan.title
                lifan_res.magnet = lifan.magnet
                lifan_res.category = lifan.category
                lifan_res.index = lifan.index
                lifan_res.save()
                return True, 1
            except:
                return False, 1
        else:
            try:
                lifan.save()
                return True, 0
            except:
                return False, 0

    # 根据标题查找裡蕃
    def _query_lifan_by_title(self,executor,title, page=1, size=-1, all=False):
        try:
            if isinstance(executor,ClientLifanExecutor):
                if all:
                    lifan_list = LifanC.select().order_by(LifanC.index).where(LifanC.title == title)
                else:
                    lifan_list = LifanC.select().order_by(LifanC.index).where(LifanC.title == title).paginate(page, size)
            else:
                if all:
                    lifan_list = LifanS.select().order_by(LifanS.index).where(LifanS.title == title)
                else:
                    lifan_list = LifanS.select().order_by(LifanS.index).where(LifanS.title == title).paginate(page, size)
        except:
            lifan_list = []
        return lifan_list

    # 根据目录名查找裡蕃
    def _query_lifan_by_category(self,executor,category, page=1, size=20, all=False):
        try:
            if isinstance(executor,ClientLifanExecutor):
                if all:
                    lifan_list = LifanC.select().order_by(LifanC.index).where(LifanC.category == category)
                else:
                    lifan_list = LifanC.select().order_by(LifanC.index).where(LifanC.category == category).paginate(page, size)
            else:
                if all:
                    lifan_list = LifanS.select().order_by(LifanS.index).where(LifanS.category == category)
                else:
                    lifan_list = LifanS.select().order_by(LifanS.index).where(LifanS.category == category).paginate(page, size)
        except:
            lifan_list = []
        return lifan_list

    # 根据序号查找目录
    def _query_category_by_index(self, index, page=1, size=-1, all=False):
        try:
            if all:
                category_list = Category.select().where(Category.index == index)
            else:
                category_list = Category.select().where(Category.index == index).paginate(page, size)
        except:
            category_list = []
        return category_list

    # 获取目录列表
    def _get_all_category(self):
        try:
            category_list = Category.select().order_by(Category.index.desc())
        except:
            category_list = []
        return category_list

# lifan服务端数据库操作类
class ServerLifanExecutor(DbExecutor):

    def save_lifanS(self,lifanS):
        return self._save_lifan(lifanS)

    def query_lifanS_by_title(self, title, page=1, size=-1, all=False):
        return self._query_lifan_by_title(self,title, page, size, all)

    def query_lifanS_by_category(self, category, page=1, size=-1, all=False):
        return self._query_lifan_by_category(self,category, page, size, all)

    def delete_lifanS_by_category(self,category):
        return self._delete_lifan_by_category(self,category)

    def delete_lifanS_by_title(self,title):
        return self._delete_lifan_by_title(self,title)

# lifan客户端数据库操作类
class ClientLifanExecutor(DbExecutor):

    def save_lifanC(self, lifanC):
        return self._save_lifan(lifanC)

    def query_lifanC_by_title(self, title, page=1, size=-1, all=False):
        return self._query_lifan_by_title(self,title,page, size, all)

    def query_lifanC_by_category(self, category, page=1, size=-1, all=False):
        return self._query_lifan_by_category(self,category, page, size, all)

    def delete_lifanC_by_category(self,category):
        return self._delete_lifan_by_category(self,category)

    def delete_lifanC_by_title(self,title):
        return self._delete_lifan_by_title(self,title)

# 目录链接类数据库操作类
class CategoryExecutor(DbExecutor):

    def save_category(self,category):
        return self._save_category(category)

    def query_category_by_index(self, index, page=1, size=-1, all=False):
        return self._query_category_by_index(index,page,size,all)

    def delete_category_by_name(self,name):
        return self._delete_category_by_index(name)

    def get_all_category(self):
        return self._get_all_category()
#
# if __name__ == '__main__':
#     pass




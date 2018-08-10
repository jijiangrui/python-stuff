#coding=utf-8
#。—————————————————————————————————————————— 
#。                                           
#。  db_executor.py                               
#。                                           
#。 @Time    : 2018/8/9 01:22                
#。 @Author  : capton                        
#。 @Software: PyCharm                
#。 @Blog    : http://ccapton.cn              
#。 @Github  : https://github.com/ccapton     
#。 @Email   : chenweibin1125@foxmail.com     
#。__________________________________________


from models import *

class DbExecutor:

    def save_AqiyiVmovieModel(self, aqiyiVmovieModel):
        try:
            res = IqiyiVmovieModel.get(IqiyiVmovieModel.name == aqiyiVmovieModel.name)
        except DoesNotExist:
            res = None
        if res:
            try:
                res.name = IqiyiVmovieModel.name
                res.area = IqiyiVmovieModel.area
                res.movie_type = IqiyiVmovieModel.movie_type
                res.movie_standard = IqiyiVmovieModel.movie_standard
                res.generation = IqiyiVmovieModel.generation
                res.actors = IqiyiVmovieModel.actors
                res.url_type = IqiyiVmovieModel.url_type
                res.url = IqiyiVmovieModel.url
                res.update_time = IqiyiVmovieModel.update_time
                res.save()
                return True, 1
            except:
                return False, 1
        else:
            try:
                aqiyiVmovieModel.save()
                return True, 0
            except:
                return False, 0

    # 根据标题查找裡蕃
    def query_aqiyiVmovieModel_by_area(self, area, page=1, size=-1, all=False):
        try:
            if all:
                model_list = IqiyiVmovieModel.select().order_by(IqiyiVmovieModel.update_time)\
                    .where(IqiyiVmovieModel.area == area)
            else:
                model_list = IqiyiVmovieModel.select().order_by(IqiyiVmovieModel.update_time)\
                    .where(IqiyiVmovieModel.area == area).paginate(page,size)
        except:
            model_list = []
        return model_list

    def query_aqiyiVmovieModel_by_standard(self, standard, page=1, size=-1, all=False):
        try:
            if all:
                model_list = IqiyiVmovieModel.select().order_by(IqiyiVmovieModel.update_time)\
                    .where(IqiyiVmovieModel.movie_standard == standard)
            else:
                model_list = IqiyiVmovieModel.select().order_by(IqiyiVmovieModel.update_time)\
                    .where(IqiyiVmovieModel.movie_standard == standard).paginate(page,size)
        except:
            model_list = []
        return model_list

    def query_aqiyiVmovieModel_by_videotype(self, video_type, page=1, size=-1, all=False):
        try:
            if all:
                model_list = IqiyiVmovieModel.select().order_by(IqiyiVmovieModel.update_time)\
                    .where(IqiyiVmovieModel.movie_type == video_type)
            else:
                model_list = IqiyiVmovieModel.select().order_by(IqiyiVmovieModel.update_time)\
                    .where(IqiyiVmovieModel.movie_type == video_type).paginate(page,size)
        except:
            model_list = []
        return model_list

    def query_aqiyiVmovieModel_by_generation(self, generation, page=1, size=-1, all=False):
        try:
            if all:
                model_list = IqiyiVmovieModel.select().order_by(IqiyiVmovieModel.update_time)\
                    .where(IqiyiVmovieModel.generation == generation)
            else:
                model_list = IqiyiVmovieModel.select().order_by(IqiyiVmovieModel.update_time)\
                    .where(IqiyiVmovieModel.generation == generation).paginate(page,size)
        except:
            model_list = []
        return model_list
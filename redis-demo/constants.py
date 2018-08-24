#coding=utf-8
#。—————————————————————————————————————————— 
#。                                           
#。  constants.py                               
#。                                           
#。 @Time    : 2018/8/8 23:24                
#。 @Author  : capton                        
#。 @Software: PyCharm                
#。 @Blog    : http://ccapton.cn              
#。 @Github  : https://github.com/ccapton     
#。 @Email   : chenweibin1125@foxmail.com     
#。__________________________________________

db_save_path = 'db/data'


# http://list.iqiyi.com/www/1/28997----------2---24-1-1-iqiyi--.html

iqiayi_constants = {

    'iqiyi_vmovie_list_baseurl':'http://list.iqiyi.com/www/1',

    'areas' : [
    ('1','华语'),
    ('28997','香港'),
    ('2','美国'),
    ('3','欧洲'),
    ('4','韩国'),
    ('308','日本'),
    ('1115','泰国'),
    ('5','其他'),
    ],

    'movie_type':[
    ('8','喜剧'),
    ('13','悲剧'),
    ('6','爱情'),
    ('11','动作'),
    ('131','枪战'),
    ('291','犯罪'),
    ('128','惊悚'),
    ('10','恐怖'),
    ('289','悬疑'),
    ('12','动画'),
    ('27356','家庭'),
    ('1284','奇幻'),
    ('129','魔幻'),
    ('9','科幻'),
    ('7','战争'),
    ('130','青春'),
    ],

    'movie_standard':[
        ('27397','巨制'),
        ('27815','院线'),
        ('30149','独播'),
        ('27041','网络大电影'),
        ('27976','经典'),
        ('27977','口碑佳片'),
        ('29745','4K'),
        ('296','原生'),
        ('311','粤语'),
    ],

    'generation':[
        ('2018','2018'),
        ('2017','2017'),
        ('2016','2016'),
        ('2011_2015','2015-2011'),
        ('2000_2010','2010-2000'),
        ('1990_1999','90年代'),
        ('1980_1989','80年代'),
        ('1964_1979','更早'),
    ]
}

def get_iqiyi_vmovie_list(page=1):
    baseurl = iqiayi_constants.get('iqiyi_vmovie_list_baseurl')
    url_list = []
    category_list = []
    for areas in iqiayi_constants.get('areas'):
        part1 = '/'+ areas[0]
        category1 = areas[1]+ ' '
        for movie_type in iqiayi_constants.get('movie_type'):
            part2 = part1 + '-' +movie_type[0]
            category2 = category1 + movie_type[1] + ' '
            for movie_standard in iqiayi_constants.get('movie_standard'):
                part3 = part2 + '-'*5 + movie_standard[0]
                category3 = category2 + movie_standard[1] + ' '
                for generation in iqiayi_constants.get('generation'):
                    part4 = part3+'-'*4+'2-'+ generation[0] + '--24-'+str(page)+'-1-iqiyi--.html'
                    category_final = category3 + generation[1]
                    url_list.append(baseurl+part4)
                    category_list.append(category_final)
    return url_list,category_list

    # /1-8-----27401----2-2018--24-1-1-iqiyi--.html


if __name__ == '__main__':

    for url in get_iqiyi_vmovie_list(1)[0]:
        print(url)

    print(len(get_iqiyi_vmovie_list(1)[0]))





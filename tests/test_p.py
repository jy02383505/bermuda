# -*- coding: utf-8 -*-
import urllib
from random import Random
from multiprocessing import Process
import httplib
import urllib2
import datetime
import simplejson as json
import time
import codecs
# import sys

# reload(sys)
# sys.setdefaultencoding("utf-8")

def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str
#用DHC提交时，内容要用双引号
def do_post():
    # conn = httplib.HTTPConnection("223.202.45.190")
    conn = httplib.HTTPConnection("r.chinacache.com")
    # conn = httplib.HTTPConnection("223.202.52.83")
    headers = {"Content-type":"application/json"}
    for i in range(15,16):
        # params = ({"username": "rdbrd","password": "Rdbrd123","speed": "","startTime": "","validationType": "MD5","isOverride ": 1,"tasks": [{"id":"124","url": "http://rdbtest1.ccgslb.net/QtXml4.dll","md5": "c53df18d306639f9fd424f8046346144"}]})
        # params = ({"username": "meituan","password": "MTmt123","speed": "","startTime": "","validationType": "BASIC","isOverride ": 1,"tasks": [{"id": i,"url": "http://*.mtmos.com/index.html"}]})
        # params = ({"username": "dawx","password": "s0oUU0du$P","speed": "","startTime": "","validationType": "BASIC","isOverride ": 1,"tasks": [{"id": i,"url": "http://jiang.dawx.com/app100688853/sgonline022001/swf_new/tipsui.swf"}]})
        # params = ({"username": "dawx","password": "s0oUU0
        # du$P","speed": "","startTime": "","validationType": "BASIC","isOverride ": 1,"tasks": [{"id":"1393335719102","url": "http://jiang.dawx.com/app100688853-000/sgonline022001/swf_new/tipsui.swf"}]})
        # params = ({'username': 'cztv', 'tasks': [{'url': 'http://video.cztv.com/cztv/vod/2015/06/23/6bbc845aa3094e039417a11ee17b9769/h264_1500k_mp4.mp4', 'id': '116233'},{'url': 'http://video.cztv.com/cztv/vod/2015/06/23/6bbc845aa3094e039417a11ee17b9769/h264_800k_mp4.mp4', 'id': '116234'},{'id': '116235','url': 'http://video.cztv.com/cztv/vod/2015/06/23/6bbc845aa3094e039417a11ee17b9769/h264_450k_mp4.mp4'},{'url': 'http://video.cztv.com/cztv/vod/2015/06/20/1532ef44abd24cecb760d219b8be7486/h264_1500k_mp4.mp4', 'id': '70821'},{'url': 'http://video.cztv.com/cztv/vod/2015/06/20/1532ef44abd24cecb760d219b8be7486/h264_800k_mp4.mp4', 'id': '70822'},{'id': '70823','url': 'http://video.cztv.com/cztv/vod/2015/06/20/1532ef44abd24cecb760d219b8be7486/h264_450k_mp4.mp4'}], 'nest_track_level': 0, 'startTime': '', 'validationType': 'BASIC', 'password': '(8cT29JL7r', 'speed': ''})
        # params = ({'username': 'cztv', 'tasks': [{'url': 'http://video.cztv.com/cztv/vod/2015/06/20/1532ef44abd24cecb760d219b8be7486/h264_1500k_mp4.mp4', 'id': '70821'},{'url': 'http://video.cztv.com/cztv/vod/2015/06/20/1532ef44abd24cecb760d219b8be7486/h264_800k_mp4.mp4', 'id': '70822'},{'id': '70823','url': 'http://video.cztv.com/cztv/vod/2015/06/20/1532ef44abd24cecb760d219b8be7486/h264_450k_mp4.mp4'}], 'nest_track_level': 0, 'startTime': '', 'validationType': 'BASIC', 'password': '(8cT29JL7r', 'speed': ''})
        # params = ({"username": "vxinyou","password": "1234@xinyou","speed": "1980.123k","validationType": "BASIC","isOverride ": 1,"tasks": [{"id": i,"url": "http://mlftp.vxinyou.com/1.14.0/data0_1.16.0.epk"}]})
        # params = ({'username': 'rdbrd', 'parent':'rdbrd',"compressed": True,'tasks': [{'url': 'http://rdbtest2.ccgslb.net/1.txt', 'id': '1142733'}], 'nest_track_level': 0, 'startTime': '', 'validationType': 'BASIC', 'password': 'Rdbrd123', 'speed': ''})
        # params = ({'username': 'cnlive', 'parent':'people','isSub':'True','tasks': [{'url': 'http://video02.cnlive.com/video/data1/2015/0921/74026/301/b179c7d831054f08b14da860fa5dfb3c_74026_30111.m3u8', 'id': '1142733'}], 'nest_track_level': 0, 'startTime': '', 'validationType': 'BASIC', 'password': 'People@123', 'speed': ''})
        params = ({'username': 'verycd', 'tasks': [{'url': 'http://uri.xdcdn.net/jsk/file/8d5b52c30ded5b82e7e506784189ce52d4388bc8/sharedassets0.assets.lz', 'id': '49543'}], 'nest_track_level': 0, 'startTime': '', 'validationType': 'BASIC', 'password': '(8cT29JL7r', 'speed': ''})
        # params = ({'username': 'cztv', 'tasks': [{'url': 'http://v2.cztv.com/cztv/vod/2015/08/18/5EF106BB76064eaeA0B7B4E9F6B2C442/h264_1500k_mp4.mp4', 'id': '49543'},{'url': 'http://v2.cztv.com/cztv/vod/2015/08/03/373caa3e65cc431a83b91f0bd62caacf/h264_450k_mp4.mp4', 'id': '49544'},{'url': 'http://v2.cztv.com/cztv/vod/2015/08/03/101557950bb24e01bff169c932d15e1c/h264_1500k_mp4.mp4', 'id': '49545'},{'url': 'http://v2.cztv.com/cztv/vod/2015/08/03/101557950bb24e01bff169c932d15e1c/h264_800k_mp4.mp4', 'id': '49546'},{'url': 'http://v2.cztv.com/cztv/vod/2015/08/03/101557950bb24e01bff169c932d15e1c/h264_450k_mp4.mp4', 'id': '49547'},{'url': 'http://v2.cztv.com/cztv/vod/2015/07/29/5ad31b6dc3044a068798f415834e72cb/h264_1500k_mp4.mp4', 'id': '49548'},{'url': 'http://v2.cztv.com/cztv/vod/2015/07/29/5ad31b6dc3044a068798f415834e72cb/h264_800k_mp4.mp4', 'id': '49549'},{'url': 'http://v2.cztv.com/cztv/vod/2015/07/29/5ad31b6dc3044a068798f415834e72cb/h264_450k_mp4.mp4', 'id': '49550'}], 'nest_track_level': 0, 'startTime': '', 'validationType': 'BASIC', 'password': '(8cT29JL7r', 'speed': ''})
        # params = ({"username": "vxinyou","password": "1234@xinyou","speed": "1980.123k","validationType": "BASIC","isOverride ": 1,"tasks": [{"id": i,"url": "http://mlftp.vxinyou.com/1.14.0/data0_1.16.0.epk"}]})
        # params = ({"username": "baidu-91","password": "s5I*QbXg6M","speed": "1980.123k","startTime": "","validationType": "BASIC","isOverride ": 1,"tasks": [{"id": i,"url": "http://apk.r1.market.hiapk.com/data/upload/apkpatch/2014/6_14/14/6b3a8c6b-d2c1-47f8-8e5a-d71994817836.patch"}]})
        # params = ({"username": "baidu-91","password": "s5I*QbXg6M","speed": "","startTime": "","validationType": "BASIC","isOverride ": 1,"tasks": [{"id": i,"url": "http://apk.r1.market.hiapk.com/data/upload/apkpatch/2014/6_14/14000/6b3a8c6b-d2c1-47f8-8e5a-d71994817836.patch"}]})
        # params = ({"username": "baidu-91","password": "s5I*QbXg6M","speed": "600.456k","startTime": "","validationType": "MD5","isOverride ": 1,"tasks": [{"id": i,"md5":"47e9e575b97df2078165cafb73f9cbbd","url": "http://apk.r1.market.hiapk.com/data/upload/apkpatch/2014/6_14/14/6b3a8c6b-d2c1-47f8-8e5a-d71994817836.patch"}]})
        # params = ({"username": "baidu-91","password": "s5I*QbXg6M","speed": "","startTime": "2014-07-07 17:18:00","validationType": "MD5","isOverride ": 1,"tasks": [{"id": i,"md5":"47e9e575b97df2078165cafb73f9cbbd","url": "http://apk.r1.market.hiapk.com/data/upload/apkpatch/2014/6_14/14/6b3a8c6b-d2c1-47f8-8e5a-d71994817836.patch"}]})
        # conn.request("POST", "/content/preload", json.JSONEncoder().encode(params), headers)
        conn.request("POST", "/internal/preload", json.JSONEncoder().encode(params), headers)
        response = conn.getresponse()
        print response.read()
        #params_2 = urllib.urlencode({'558a46ea2b8a68be466c1ddcusername': 'sina_t', 'password': 'MTE3YjU2ZTlhNmNl', 'task': '{"urls":["http://ww4.sinaimg.cn/bmiddle/61b69811gw1dld19fhhelj.jpg","http://ww4.sinaimg.cn/mw600/6f40d48agw1dpzmm9vtozj.jpg","http://ww4.sinaimg.cn/thumbnail/6dceb033jw1doxgrr5z7hj.jpg","http://ww4.sinaimg.cn/thumbnail/62d8a08bjw1dqwyqv2lg6j.jpg"]}'})
        #params_2 = urllib.urlencode({'username': 'snda', 'password': 'ptyy@snda.com', 'task': '{"dirs":["http://shengdafds.peixin.ccgslb.net/test/","http://gfxz.autopatch.sdo.com/test","http://launcher.autopatch.sdo.com/test"],"callback":{"url":"http://www.a.com/listener","email":["dongling.zhang@chinacache.com","zdl__2007@126.com"],"acptNotice":true}}'})
        #f_2 = urllib.urlopen("http://223.202.45.190/content/refresh" , params_2)
        #f_2 = urllib.urlopen("http://192.168.158.15:8000/content/refresh" , params_2)
    conn.close()
    # params = ({"username": "baidu-91","password": "s5I*QbXg6M","speed": "1980.123k","startTime": "","validationType": "BASIC","isOverride ": 1,"tasks": [{"id": i,"url": "http://apk.r1.market.hiapk.com/data/upload/apkpatch/2014/6_14/14/6b3a8c6b-d2c1-47f8-8e5a-d71994817836.patch"}]})
# params ={'username':'verycd','password':'verycd@cc','task':[{"id":"4698647","url":"http://uri.xdcdn.net/syk/file/67706107435cc55ed8850ceee06b3fcf798caccb/file_list.txt"},{"id":"4698649","url":"http://uri.xdcdn.net/syk/file/2cc51148537ccbe2b7251448fbf5a08816a60cd3/preLoad.swf"}]}

if __name__ == '__main__':
    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    #####submit a piece of preload task#####
    do_post()

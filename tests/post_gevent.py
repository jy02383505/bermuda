#! -*- coding=utf-8 -*-
"""
@version: ??
@author: rubin
@license:
@contact: longjun.zhao@chinacache.com
@site: 
@software: PyCharm
@file: post_gevent.py
@time: 17-6-27 下午7:10

"""
import urllib
import json
from gevent import monkey; monkey.patch_all()
import gevent



def do_post(str_t):
    for i in range(0, 1):
        urls = []
        for j in range(1):
            urls.append('http://mso.chinacache.net/22_%s/%s.html' % (str_t, str(j)))
        task = json.dumps({"urls": urls})

        params = urllib.urlencode({'username': 'chinacache','password': 'aPi@jd.com_Purge','task': task})


        print params

        f = urllib.urlopen("http://223.202.203.52:81/internal/refresh", params)

        print f.read()

list_gevent = []

for i in range(1):
    list_gevent.append(gevent.spawn(do_post, str(i)))

gevent.joinall(list_gevent)




if __name__ == "__main__":
    pass
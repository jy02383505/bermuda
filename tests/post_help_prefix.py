#! -*- coding=utf-8 -*-
"""
@version: ??
@author: rubin
@license:
@contact: longjun.zhao@chinacache.com
@site: 
@software: PyCharm
@file: post_help_prefix.py
@time: 17-6-13 下午1:50
"""
# encoding=utf-8

import urllib
# from multiprocessing import Process
import json
import traceback
import time
def do_post_internal():
    for i in range(0, 1):
        task = json.dumps({'urls': ['https://www.zhangyuelicai.com/test1/hydt/1.html', 'https://www.zhangyuelicai.com/tesfdfd/hydt/1.html']})

        params = urllib.urlencode({'username': 'shws', 'password': '', 'task': task})


        print params

        # f = urllib.urlopen("http://223.202.203.52/content/refresh", params)
        f = urllib.urlopen("http://223.202.203.52/internal/refresh", params)

        print f.read()


def do_post_content():
    for i in range(0, 1):
        task = json.dumps({'urls': ['https://www.zhangyuelicai.com/test1/hydt/1.html', 'https://www.zhangyuelicai.com/tesfdfd/hydt/1.html']})

        params = urllib.urlencode({'username': 'shws', 'password': '', 'task': task})


        print params

        # f = urllib.urlopen("http://223.202.203.52/content/refresh", params)
        f = urllib.urlopen("http://223.202.203.52/internal/refresh", params)

        print f.read()


def do_post_read_file(file_name):
    """

    Args:
        file_name:

    Returns:

    """
    url_list = []
    try:
        with open(file_name) as f1:
            while True:
                line = f1.readline()
                if line:
                    url_list.append(line.strip())
                else:
                    break
    except Exception, e:
        print traceback.format_exc(e)
    return url_list


def do_post_internal_new(url_list_temp):
    for i in range(0, 1):
        task = json.dumps({'urls': url_list_temp})

        params = urllib.urlencode({'username': 'cnkang', 'password': '', 'task': task})


        print params

        # f = urllib.urlopen("http://223.202.203.52/content/refresh", params)
        f = urllib.urlopen("http://r.chinacache.com/internal/refresh", params)

        print f.read()

def do_post_new(file_name):
    url_list = do_post_read_file(file_name)
    url_temp = []
    i = 0
    success = 0
    failed = 0
    for url in url_list:
        i += 1

        print "send number:%s" % i
        url_temp.append(url)

        if len(url_temp) >= 50:
            print "send i:%s" %i
            try:
                do_post_internal_new(url_temp)
            except Exception, e:
                print("send error e:%s" % e)
                failed += len(url_temp)
            success += len(url_temp)
            url_temp=[]
            time.sleep(1)
    try:
        do_post_internal_new(url_temp)
    except Exception, e:
        print("send error e:%s" % e)
        failed += len(url_temp)
    success += len(url_temp)
    print "success:%s" % success
    print "failed:%s" % failed






if __name__ == '__main__':
    # for i in range(1):
    #      Process(target=do_post_new).start()
    do_post_new("a.test")

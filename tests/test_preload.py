#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 'vance' on '11/14/14'.

__doc__ = ''
__ver__ = '1.0'
__author__ = 'vance'

import urllib
from random import Random
from multiprocessing import Process
import httplib
import urllib2
import datetime
import simplejson as json
from flask.helpers import jsonify
import unittest
import nose
from nose.tools import (
    assert_dict_equal,
    assert_equal,
    assert_false,
    assert_in,
    assert_is_instance,
    assert_is_not_none,
    assert_list_equal,
    assert_not_in,
    assert_raises,
    assert_true,
)


def do_post():
    url='http://223.202.52.43/internal/preload/search'
    params = '{"endNo":15,"finishTime":{"endTime":"","startTime":""},' \
             '"isSub":false,"parent":"qq","startNo":1,' \
             '"startTime":{"endTime":"","startTime":""},' \
             '"status":null,"url":"","username":"qq"}'
    data = json.loads(params)
    # if data.get('isSub', False):
    #         message = {}
    #         task_list, invalids = get_preload_new(request)
    #         if task_list:
    #             queue.put_json2("preload_task", task_list)
    #             if invalids:
    #                 message['code'] = 201
    #                 message['invalids'] = invalids
    #             else:
    #                 message['code'] = 0
    #                 message['msg'] = 'ok'
    #         else:
    #             message['code'] = 202
    #             message['msg'] = 'urls is error'
    #         return jsonify(message)
    #     else:
    #         for task in data.get('tasks'):
    #             pass
            #     channel_name = get_channelname_from_url(task.get('url', ''))
            #     pre_dev = PRELOAD_DEVS.get(channel_name)
            #     if not pre_dev:
            #         logger.debug('%s not config channel' % channel_name)
            #         raise ChannelError('%s not config channel' % channel_name)
            # queue.put_json2("preload_task", get_preload(request))
            # return jsonify({"code": 0, "msg": "ok"})
    # for i in range(0, 1):
        # conn = httplib.HTTPConnection("223.202.52.77")
        #params = urllib.urlencode({'username': 'duowan', 'password': "5VGO3LB62O", 'task': '{"urls":["http://downhdlogo.yy.com/seicard/basic/280/210/20/0380206713/c380206713ZwRoyAsF.png"]}'})
        #params = urllib.urlencode({'username': 'duowan', 'task': '{"urls":["http://downhdlogo.yy.com/seicard/basic/280/210/20/0380206713/c380206713ZwRoyAsF.png"]}'})
        #params = {'username':'verycd','password':'verycd@cc','task': '[1,2,3]',}
        # headers = {'content-type': 'application/json'}
        #r = requests.post('http://223.202.52.77/content/refresh', json.dumps(params), headers=headers)

        # url = 'http://223.202.52.83/%s' % router
        # #url ='http://r.chinacache.com/%s'%router
        # print url, params
        # conn.request("POST", "/content/preload", json.JSONEncoder().encode(params), headers)
        # response = conn.getresponse()
        # print response.read()

        # r = requests.post(url, data=json.dumps(params))
        # #r = requests.post(url, json.dumps(params),headers=headers)
        # #f = urllib.urlopen("http://223.202.52.77/internal/refresh" , params)
        # #f = urllib.urlopen("http://223.202.52.77/content/refresh" , params)
        # print r.text
        # return json.loads(r.text)
        #print f.read()


# class MyTestCase(unittest.TestCase):
#     def setUp(self):
#         print "TC setUp %s" % self
#
#     def tearDown(self):
#         print "TC tearDown %s" % self
#
#     def test_receiver_new_proload(self):
#         """
#         post json:
#         {
#             "username": "chinacache",
#             "password": “123654”，
#             "speed": "200k",
#             "startTime": "2013-05-02 18:43:03",
#             "validationType": "MD5",
#             “nest_track_level”:0，
#             "tasks": [
#                 {
#                     "id": "001",
#                     "url": "http://xxxx.com/test/a.txt",
#                     "md5": "d6a359b32979902a12f60b2a149e4a55"
#                 },
#                 {
#                     "id": "002",
#                     "url": "http://xxxx.com/test/b.txt",
#                     "md5": "d6a359b32979902a12f60b2a149e4a55"
#                 }
#             ]
#         }
#         return:
#         {
#             "code": 0,
#             "msg": "ok"
#         }
#         """
#         params = {"username": "verycd", "password": "verycd@cc", "tasks": [{"id": "4698647",
#                                                                             "url": "http://uri.xdcdn.net/syk/file/67706107435cc55ed8850ceee06b3fcf798caccb/file_list.txt"},
#                                                                            {"id": "4698649",
#                                                                             "url": "http://uri.xdcdn.net/syk/file/2cc51148537ccbe2b7251448fbf5a08816a60cd3/preLoad.swf"}]}
#         # params = ({"username": "baidu-91","password": "s5I*QbXg6M","speed": "1500.5k","startTime": "2014-10-15 16:45:00","validationType": "MD5","isOverride ": 1,"tasks": [{"id": i,"md5":"8359abd974a48d3aba09e14e7eef5968","url": "http://apk.r1.market.hiapk.com/data/upload/2014/10_15/13/com.widdit.base_134950.apk"}]})
#         router = '/content/preload'
#
#         message = {
#             "code": 0,
#             "msg": "ok"
#         }
#         assert_dict_equal(message, do_post(router, params))
#
#     def test_query_task_api(self):
#         """
#         post json:
#         {'username':'verycd',
#          'password':'verycd@cc',
#          'tasks': '[1,2,3]',
#          # 'created_time':'2014-11-14 14:00:00',
#          'status':[TIMER,PROGRESS,INVALID,FINISHED,FAILED]
#         }
#         return:
#         {
#         total_count: xxx
#         task:[
#         {'task_id':xxx
#         'url':xxx
#         'status':xxx
#         'percent':xxx},
#         {.....},......
#         ]
#
#         }
#         """
#         # for i in range(1):
#         # Process(target=do_post).start()
#         router = 'content/preload/search'
#         params = {"username": "verycd", "password": "verycd@cc", "tasks": ["4698699", "4698673", "4699075"],
#                   "status": []}
#
#         message = ["totalCount", "tasks"]
#         # re = [x.encode("utf8") for x in do_post(router,params).keys()]
#         # print type(re),re
#         assert_list_equal(message, do_post(router, params).keys())


if __name__ == '__main__':
    do_post()
    pass
    # unittest.main()
    # test = MyTestCase()
    # test.test_receiver_new_proload()

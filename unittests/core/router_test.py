# -*- coding:utf-8 -*-  
"""
Created on 2013-2-28

@author: li.chang peng.zhou
"""
import unittest
from mockito import mock, when, unstub, verify, any
from core import database
when(database).db_session().thenReturn(mock())
when(database).query_db_session().thenReturn(mock())
from core import queue
from bson.objectid import ObjectId
from datetime import datetime
import bson
import time, json
import test_data_core as test_data
from core import router
from core import dir_refresh, url_refresh

class router_way_test(unittest.TestCase):

    def setUp(self):
        self.dt = datetime(2012, 1, 1, 0, 1, 0, 000000)
        self.db = mock()
        self.db.url = mock()
        self.db.request = mock()
        self.db.device = mock()
        self.router = router.Router()
        # router.preload_worker.dispatch=mock()
        router.queue = mock()
        self.PRELOAD_MESSAGES_TIMER = [
            { 
                '_id' : '543a906a25b541639c380ac2',
                'username' : 'youmi',
                'parent': 'youmi',
                'status' : 'TIMER',
                'get_url_speed' : '1024k',
                'user_id' : '4648',
                'check_type' : 'BASIC',
                'task_id' : '1',
                'remote_addr' : '115.231.94.72',
                'url' : u'http://owan-img.ymapp.com/img/fuck1.jpg',
                'preload_address' : '127.0.0.1:80',
                'priority' : 0,
                'nest_track_level' : 0,
                'dev_id' : '543a906a25b541639c380ac1',
                'is_multilayer' : False,
                'action' : 'refresh,preload',
                'md5' : '',
                'channel_code' : '56634',
                'start_time': datetime(2014, 11, 1, 0, 0),
                'created_time': datetime(2014, 12, 1, 0, 0)
            }
        ]


    def tearDown(self):
        unstub()
        unittest.TestCase.tearDown(self)

    def test_merge_urlMsg(self):
        for url in test_data.MESSAGES:
            self.router.merge_urlMsg(url)
        self.assertEquals(test_data.MERGED_URL, self.router.merged_urls)

        router.url_refresh.work = mock()

        for index in range(len(test_data.MESSAGES_DIR)):
            when(router.url_refresh.work).delay([test_data.MESSAGES_DIR[index]]).thenReturn("ok")
            self.router.merge_urlMsg(test_data.MESSAGES_DIR[index])
            verify(url_refresh.work).delay([test_data.MESSAGES_DIR[index]])
        

    def test_refresh_router_url(self):
        router.url_refresh.work = mock()
        router.queue = mock()
        MESSAGES_STR = [json.dumps(url) for url in test_data.MESSAGES]
        when(router.queue).get('url_queue', 5000).thenReturn(MESSAGES_STR)
        for key, value in self.router.merged_urls.iteritems():
            when(router.url_refresh.work).delay(value).thenReturn("ok")
        self.router.refresh_router()
        self.assertEquals(test_data.MERGED_URL, self.router.merged_urls)
        for key, value in self.router.merged_urls.iteritems():
            verify(router.url_refresh.work).delay(test_data.MERGED_URL.get(key))

    def test_refresh_router_dir(self):
        router.url_refresh.work = mock()
        router.queue = mock()
        MESSAGES_DIR_STR = [json.dumps(url) for url in test_data.MESSAGES_DIR]
        when(router.queue).get('url_queue', 5000).thenReturn(MESSAGES_DIR_STR)
        for index in range(len(test_data.MESSAGES_DIR)):
            when(router.dir_refresh.work).delay(test_data.MESSAGES_DIR[index]).thenReturn("ok")
        self.router.refresh_router()
        self.assertEquals({}, self.router.merged_urls)

        for index in range(len(test_data.MESSAGES_DIR)):
            verify(dir_refresh.work).delay(test_data.MESSAGES_DIR[index])

    def test_merge_preload_task(self):
        url_dict = {}
        url_other = []
        for url in test_data.PRELOAD_MESSAGES:
            self.router.merge_preload_task(json.dumps(url), url_dict, url_other)
        self.assertEquals(test_data.PRELOAD_MESSAGES_URL, url_dict)
        self.assertEquals(self.PRELOAD_MESSAGES_TIMER, url_other)

    def test_preload_router(self):

        when(router.database).db_session().thenReturn(mock())
        router.database.db_session().preload_url = mock()
        PRELOAD_MESSAGES_STR = [json.dumps(url) for url in test_data.PRELOAD_MESSAGES]
        when(router.queue).get('preload_task', 5000).thenReturn(PRELOAD_MESSAGES_STR)
        when(router.database.db_session().preload_url).insert(self.PRELOAD_MESSAGES_TIMER).thenReturn("ok")
        for values in test_data.PRELOAD_MESSAGES_URL.values():
            when(router.preload_worker.dispatch).delay(values).thenReturn("ok")
        self.router.preload_router()
        for values in test_data.PRELOAD_MESSAGES_URL.values():
            verify(router.preload_worker.dispatch).delay(values)
        verify(router.database.db_session().preload_url).insert(self.PRELOAD_MESSAGES_TIMER)

if __name__ == "__main__":
    unittest.main()

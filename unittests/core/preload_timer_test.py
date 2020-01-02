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
from core import preload_timer

class preload_timer_test(unittest.TestCase):

    def setUp(self):
        self.dt = datetime(2012, 1, 1, 0, 1, 0, 000000)
        preload_timer.datetime = mock()
        when(preload_timer.datetime).now().thenReturn(self.dt)
        when(preload_timer.database).query_db_session().thenReturn(mock())
        when(preload_timer.database).db_session().thenReturn(mock())
        self.timers = preload_timer.Timers()
        when(preload_timer.preload_worker).dispatch().thenReturn()
    def tearDown(self):
        unstub()
        unittest.TestCase.tearDown(self)

    def test_reset(self):
        self.timers.db.preload_url = mock()
        when(self.timers.db.preload_url).remove({"_id": '543a906a25b541639c380ac2'}).thenReturn('ok')
        result = self.timers.reset(test_data.PRELOAD_MESSAGES_TIMER[0])
        self.assertEquals(test_data.PRELOAD_MESSAGES_TIMER_PROGRESS[0], result)
        verify(self.timers.db.preload_url).remove({"_id": '543a906a25b541639c380ac2'})

    def test_merge_preload_task(self):
        url_dict = {}
        self.timers.merge_preload_task(test_data.PRELOAD_MESSAGES_PROGRESS, url_dict)
        self.assertEquals(url_dict, test_data.PRELOAD_MESSAGES_URL)

    def test_timer_run(self):
        self.timers.query_db.preload_url = mock()
        when(self.timers.query_db.preload_url).find({"status": "TIMER", "start_time": {"$lte": self.dt}}).thenReturn(test_data.PRELOAD_MESSAGES_TIMER)
        self.timers.db.preload_url = mock()
        when(self.timers.db.preload_url).remove({"_id": '543a906a25b541639c380ac2'}).thenReturn('ok')

        when(preload_timer.preload_worker.dispatch).delay(test_data.PRELOAD_MESSAGES_TIMER_PROGRESS).thenReturn('ok')
        self.timers.timer_run()
        verify(self.timers.db.preload_url).remove({"_id": '543a906a25b541639c380ac2'})
        verify(preload_timer.preload_worker.dispatch).delay(test_data.PRELOAD_MESSAGES_TIMER_PROGRESS)

    def test_timer_run_Exception(self):
        self.timers.query_db.preload_url = mock()
        when(self.timers.query_db.preload_url).find({"status": "TIMER", "start_time": {"$lte": self.dt}}).thenReturn(Exception("This's Exception"))
        self.timers.timer_run()

if __name__ == "__main__":
    unittest.main()

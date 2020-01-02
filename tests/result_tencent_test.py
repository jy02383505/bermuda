#-*- coding:utf-8 -*-
"""
Created on 2011-6-24

@author: IBM
"""
import unittest
from receiver import result_tencent
from mockito import when, mock, verify , unstub , any
from datetime import datetime
from bson import ObjectId

ISOTIMEFORMAT = '%Y-%m-%d %X'


class Test(unittest.TestCase):
    def setUp(self):
        self.db_session = mock()
        self.db_session.url = mock()
        self.db_session.request = mock()

    def tearDown(self):
        unstub()

    def testgetResult(self):
        urls = [{"_id": 1, "r_id": ObjectId('4e4c7b9f5bc89412ec000004'), "url": "http://www.chinacache.com/a.jpg", "status": "PROGRESS", "isdir": False,
                         "finish_time": '20110624142700', "action": "purge", "is_multilayer": False,
                         "channel_code": "0005", "created_time":""},
                {"_id": 2, "r_id": ObjectId('4e4c7b9f5bc89412ec000004'), "url": "http://www.chinacache.com/u.jpg", "status": "PROGRESS", "isdir": False,
                         "finish_time": '20110624142700', "action": "expire", "is_multilayer": False,
                         "channel_code": "0005", "created_time":""},
        ]
        result = mock()

        when(self.db_session.request).find({"username": 'test', "created_time": {"$gte": datetime.strptime('20110624142500', '%Y%m%d%H%M%S'), "$lte": datetime.strptime('20110624142800', '%Y%m%d%H%M%S')}}).thenReturn(result)
        when(result).limit(1000).thenReturn([{'created_time':'2012-01-01 01:01:01', 'remote_addr':'0.0.0.1', 'serial_num':'123456', '_id':ObjectId('4e4c7b9f5bc89412ec000004')}])
        when(self.db_session.url).find({'r_id': ObjectId('4e4c7b9f5bc89412ec000004')}).thenReturn(urls)
        when(result_tencent).getStatus({"_id": 1, "r_id": ObjectId('4e4c7b9f5bc89412ec000004'), "url": "http://www.chinacache.com/a.jpg", "status": "PROGRESS", "isdir": False,
                         "finish_time": '20110624142700', "action": "purge", "is_multilayer": False,
                         "channel_code": "0005", "created_time": ""}).thenReturn(0)
        when(result_tencent).getStatus({"_id": 2, "r_id": ObjectId('4e4c7b9f5bc89412ec000004'), "url": "http://www.chinacache.com/u.jpg", "status": "PROGRESS", "isdir": False,
                         "finish_time": '20110624142700', "action": "expire", "is_multilayer": False,
                         "channel_code": "0005", "created_time": ""}).thenReturn(0)
        result_str = u'{"ret":"0","msg":"下列是URL 更新状态列表"}\n2012-01-01 01:01:01\t123456\t0.0.0.1\thttp://www.chinacache.com/a.jpg\t20110624142700\t0\t完成\n2012-01-01 01:01:01\t123456\t0.0.0.1\thttp://www.chinacache.com/u.jpg\t20110624142700\t0\t完成\n'
        # self.assertEquals(
        result_tencent.get_result(self.db_session, '20110624142500', '20110624142800', 'test')
        # , result_str)


if __name__ == "__main__":
    unittest.main()

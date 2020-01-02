# -*- coding:utf-8 -*-
__author__ = 'root'
from __init__ import *
from cache import trans_mongo_to_redis

from cache import updater_mongo_redis,trans_mongo_to_redis
when(updater_mongo_redis).ApiMongo().thenReturn(mock())
username='workercn'
channel_code='98765'
class UpdaterRedisTest(unittest.TestCase):
    def setUp(self):
        self.apimongo=mock()
        when(trans_mongo_to_redis).ApiMongo().thenReturn(self.apimongo)
        updater_mongo_redis.apimongo=mock()
        trans_mongo_to_redis.rediscache=mock()
        self.updater= updater_mongo_redis.UpdaterRedis()

    def updateMongoRedis_rcms(self):

        when(self.apimongo).sync_allObjects_rcms()
        updater_mongo_redis.sync_rcms()
        verify(self.apimongo).sync_allObjects_rcms()

    def test_updateMongoRedis_portal(self):
        when(self.apimongo).sync_allObjects_portal()
        updater_mongo_redis.sync_portal()
        verify(self.apimongo).sync_allObjects_portal()

    def tearDown(self):
            unstub()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

# -*- coding:utf-8 -*-
__author__ = 'root'
from __init__ import *
from cache import trans_mongo_to_redis
from cache.trans_mongo_to_redis import MongoToRedis

username='workercn'
channel_code='98765'
class MongoToRedisTest(unittest.TestCase):
    def setUp(self):
        trans_mongo_to_redis.rediscache=mock()

        trans_mongo_to_redis.ApiMongo=mock()
        self.apimock=mock()
        when(trans_mongo_to_redis).ApiMongo().thenReturn(self.apimock)

        self.mongo=MongoToRedis()

    def test_render_userInfo_mongo(self):
        customer_mongo={}
        when(self.apimock).read_customer_mongo(username).thenReturn(customer_mongo)
        when(trans_mongo_to_redis.rediscache).refresh_user_channel(username,customer_mongo)
        self.mongo.render_userInfo_mongo(username)
        verify(trans_mongo_to_redis.rediscache).refresh_user_channel(username,customer_mongo)


    def test_render_channels_mongo(self):
        channels_mongo = {}
        when(self.apimock).read_customer_mongo(username).thenReturn(channels_mongo)
        when(trans_mongo_to_redis.rediscache).refresh_user_channel(username,channels_mongo)
        self.mongo.render_channels_mongo(username)
        verify(trans_mongo_to_redis.rediscache).refresh_user_channel(username,channels_mongo)


    def test_render_devices_mongo_notfirst(self):
        devices_mongo = {}
        when(self.apimock).read_devices_mongo(channel_code).thenReturn(devices_mongo)
        when(trans_mongo_to_redis.rediscache).refresh_channel_devices(channel_code,True,devices_mongo)
        self.mongo.render_devices_mongo(channel_code,True)
        verify(trans_mongo_to_redis.rediscache).refresh_channel_devices(channel_code,True,devices_mongo)

    def test_render_devices_mongo_first(self):
        devices_mongo = {}
        when(self.apimock).read_devices_mongo(channel_code).thenReturn(devices_mongo)
        when(trans_mongo_to_redis.rediscache).read_firstLayerDevices_mongo(channel_code,True,devices_mongo)
        self.mongo.render_devices_mongo(channel_code,False)
        verify(trans_mongo_to_redis.rediscache).read_firstLayerDevices_mongo(channel_code,False,devices_mongo)


    def test_render_devices_mongo_notfirst(self):
        devices_mongo = {}
        when(self.apimock).read_devices_mongo(channel_code).thenReturn(devices_mongo)
        when(trans_mongo_to_redis.rediscache).refresh_channel_devices(channel_code,True,devices_mongo)
        self.mongo.render_devices_mongo(channel_code,True)
        verify(trans_mongo_to_redis.rediscache).refresh_channel_devices(channel_code,True,devices_mongo)

    def test_render_portalUserInfo_mongo(self):
        customer_mongo = {}
        when(self.apimock).read_portalChannels_mongo(username,True).thenReturn(customer_mongo)
        when(trans_mongo_to_redis.rediscache).refresh_user_channel_portal(username,customer_mongo)
        self.mongo.render_portalUserInfo_mongo(username)
        verify(trans_mongo_to_redis.rediscache).refresh_channel_devices(channel_code,True,customer_mongo)


    def tearDown(self):
            unstub()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

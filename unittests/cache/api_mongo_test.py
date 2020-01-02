# -*- coding:utf-8 -*-
import unittest
from mockito import when, mock, unstub, verify,times

import test_data
import simplejson as sjson

from util import log_utils


import  datetime
from core import database
from cache import  rediscache
when(database).db_session().thenReturn(mock())
from cache import api_mongo
from cache.api_mongo import  ApiMongo
# from cache.api_rcms import ApiRCMS
# from cache.api_portal import ApiPortal

class ApiMongoTest(unittest.TestCase):
    def setUp(self):
        api_mongo.ApiRCMS=mock()
        api_mongo.ApiPortal=mock()
        api_mongo.rediscache=mock()
        # self.ApiRCMS=mock()
        # self.ApiPortal=mock()
        dbsession=mock()
        dbsession.statistical=mock()
        when(database).db_session().thenReturn(dbsession)
        dbsession.cache_user_channels=mock()
        when(dbsession.cache_user_channels).create_index('username').thenReturn('username')
        dbsession.cache_channel_devices=mock()
        when(dbsession.cache_channel_devices).create_index('channel_code').thenReturn('channel_code')
        dbsession.cache_channel_firstlayer_devices=mock()
        when(dbsession.cache_channel_firstlayer_devices).create_index('channel_code').thenReturn('channel_code')
        dbsession.cache_user_channels_portal=mock()
        when(dbsession.cache_user_channels_portal).create_index('username').thenReturn('username')

        self.mongoapi=ApiMongo()
        self.mongoapi.read_allChannels_rcms=api_mongo.ApiRCMS.read_allChannels_rcms
        self.mongoapi.read_channels_rcms=api_mongo.ApiRCMS.read_channels_rcms
        self.mongoapi.read_devices_rcms=api_mongo.ApiRCMS.read_devices_rcms
        self.mongoapi.read_firstDevices_rcms=api_mongo.ApiRCMS.read_firstDevices_rcms
        self.mongoapi.cache_channel_devices=dbsession.cache_channel_devices
        self.mongoapi.cache_user_channels = dbsession.cache_user_channels
        self.mongoapi.cache_channel_devices=dbsession.cache_channel_devices
        self.mongoapi.cache_channel_firstlayer_devices=dbsession.cache_channel_firstlayer_devices
        self.mongoapi.cache_user_channels_portal=dbsession.cache_user_channels_portal

        api_mongo.rediscache.channels_cache=mock()
        # api_mongo.rediscache.device_cache=mock()
        # api_mongo.rediscache.firstlayer_cache=mock()

    def test_get_all_rcms_users(self):
        users_str='[{ "code": "2275", "companyName": "test", "name": "xingyun", "password": "test", "userState": "TEST" }]'
        when(self.mongoapi).read_allCustomers_rcms().thenReturn(users_str)
        len_username_arr,username_arr=self.mongoapi.get_all_rcms_users()
        self.assertEqual(len_username_arr, 1)

    def test_sync_allObjects(self):
    #     unstub()
        username ='test'
        channel_code='53831'
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        ymd=yesterday.strftime('%Y-%m-%d')
        users=[username]
        channels=[channel_code]
        username_list={'username_list':users}

        when(api_mongo.ApiRCMS).read_channels_rcms(username).thenReturn(test_data.CHANNELS)
        when(api_mongo.ApiRCMS).read_allCustomers_rcms().thenReturn(test_data.USERS)
        when(api_mongo.ApiRCMS).read_devices_rcms(channel_code).thenReturn(test_data.DEVICES)
        when(api_mongo.ApiRCMS).read_firstDevices_rcms(channel_code).thenReturn(test_data.DEVICES)
        when(api_mongo.rediscache.channels_cache).lrange(api_mongo.rediscache.USERNAME_LIST_KEY,0,-1).thenReturn([])
        chnl_rcms=sjson.JSONDecoder().decode(test_data.CHANNELS)
    #     when(api_mongo.rediscache).refresh_user_channel(username,chnl_rcms).thenReturn()
        when(self.mongoapi.statistical).find_one({"date" : ymd},{'username_list':1}).thenReturn(username_list)
    #     when(self.mongoapi.cache_user_channels).update({'username':username},{'$set':{'username':username,'channels':chnl_rcms,'time':str(datetime.datetime.now()),'needUpdateRedis':True}},upsert=True)
        when(api_mongo.rediscache).refresh_user_channel(username,chnl_rcms)

    #     chnlobj={"channels":[channel_code]}
    #     when(self.mongoapi.cache_user_channels).find_one({'username':username},{'channels':1}).thenReturn(chnlobj)
        users_str='[{ "code": "2275", "companyName": "test", "name": "xingyun", "password": "test", "userState": "TEST" }]'
        # when(self.mongoapi).get_all_rcms_users().thenReturn(1, users_str)
        when(self.mongoapi).read_allCustomers_rcms().thenReturn(users_str)
        when(self.mongoapi).sync_obj_by_multhread().thenReturn('')
        self.assertTrue(self.mongoapi.sync_allObjects_rcms(True))

    def test_sync_allObjects_portal(self):
        username='workercn'
        when(self.mongoapi).read_allCustomers_portal().thenReturn(test_data.CUSTOMER_PORTAL)
        when(self.mongoapi).read_channels_portal(u'workercn').thenReturn(test_data.CHANNELS_PORTAL)
        when(self.mongoapi.cache_user_channels_portal).find_one({"username":username}).thenReturn(test_data.CHANNEL_PORTAL_MONGO)
        api_mongo.rediscache.USERINFO_PORTAL_PREFIX=USERINFO_PORTAL_PREFIX='up_by_%s'
        mapping={}
        when(api_mongo.rediscache).refresh_customer_portal(mapping)
        self.assertTrue(self.mongoapi.sync_allObjects_portal())
    def test_sync_channels(self):
        username='workercn'
        when(self.mongoapi).read_channels_rcms(username).thenRaise(Exception('cex'))
        self.mongoapi.sync_channels(username)

    # def test_sync_allObjects_rcms(self):
    #     when(self.mongoapi).get_predays_users().thenRaise(Exception('cex'))
    #     users_str='[{ "code": "2275", "companyName": "test", "name": "xingyun", "password": "test", "userState": "TEST" }]'
    #     # when(self.api_mongo.ApiRCMS).read_allCustomers_rcms().thenReturn(users_str)
    #     when(self.mongoapi).get_all_rcms_users().thenReturn(1, users_str)
    #     #when(self.mongoapi).get_all_rcms_users().thenRaise(Exception('cex'))
    #     self.assertFalse(self.mongoapi.sync_allObjects_rcms(True))

    def test_get_predays_users(self):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        ymd=yesterday.strftime('%Y-%m-%d')
        api_mongo.rediscache.USERNAME_LIST_KEY='usernames'
        when(api_mongo.rediscache.channels_cache).smembers(api_mongo.rediscache.USERNAME_LIST_KEY).thenReturn([])
        when(self.mongoapi.statistical).find_one({"date" : ymd},{'username_list':1}).thenReturn([])
        now_str = str(datetime.datetime.now())
        num,arr=self.mongoapi.get_predays_users(1, now_str)
        self.assertEqual(num,0)
        self.assertEqual(arr,[])
    def tearDown(self):
        unstub()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
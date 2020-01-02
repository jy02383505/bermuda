__author__ = 'root'
from __init__ import *
from cache import trans_outer_to_redis
from cache.trans_outer_to_redis import OutSysToRedis
username='workercn'
channel_code='98765'
class MongoToRedisTest(unittest.TestCase):
    def setUp(self):
        trans_outer_to_redis.rediscache=mock()
        trans_outer_to_redis.ApiPortal=mock()
        trans_outer_to_redis.ApiRCMS=mock()
        when(trans_outer_to_redis).ApiPortal().thenReturn(mock())
        when(trans_outer_to_redis).ApiRCMS().thenReturn(mock())
        self.outer=OutSysToRedis()


    def test_render_userInfo_rcms(self):
        expected_rlst='xxx'
        when(self.outer.rcms_cache).read_userInfo_rcms(username).thenReturn(expected_rlst)

        rslt=self.outer.render_userInfo_outer(username,True)
        self.assertEqual(rslt,expected_rlst)

    def test_render_userInfo_portal(self):
        customer_portal='xxx'
        when(self.outer.portal_cache).read_userInfo_portal(username).thenReturn(customer_portal)
        when(trans_outer_to_redis.rediscache).refresh_user_channel_portal(username,customer_portal).thenReturn(customer_portal)
        rslt=self.outer.render_userInfo_outer(username,False)
        self.assertEqual(rslt,customer_portal)


    def test_render_channels_rcms(self):
        channels_map={}
        channels_cache='{"name":[1,2,3]}'
        when(self.outer.rcms_cache).read_channels_rcms(username).thenReturn(channels_cache)
        when(trans_outer_to_redis.rediscache).refresh_user_channel(username,json.JSONDecoder(encoding='utf-8').decode(channels_cache)).thenReturn(channels_map)
        actual_map = self.outer.render_channels_rcms(username)
        self.assertEqual(channels_map,actual_map)

    def render_devices_rcms_isnotfirst(self):
        devices_str="{'devices':['device','device1']}"
        device_list=['device','device1']
        when(self.outer.rcms_cache).read_devices_rcms(channel_code).thenReturn(devices_str)
        when(trans_outer_to_redis.rediscache).refresh_channel_devices(channel_code,True,device_list).thenReturn(device_list)
        device_list_act=self.outer.render_devices_rcms(channel_code,isNotFirst=True)
        self.assertEqual(device_list,device_list_act)

    def render_devices_rcms_isfirst(self):
        devices_str="{'devices':['device','device1']}"
        device_list=['device','device1']
        when(self.outer.rcms_cache).read_firstDevices_rcms(channel_code).thenReturn(devices_str)
        when(trans_outer_to_redis.rediscache).refresh_channel_devices(channel_code,False,device_list).thenReturn(device_list)
        device_list_act=self.outer.render_devices_rcms(channel_code,isNotFirst=False)
        self.assertEqual(device_list,device_list_act)
    def render_devices_rcms_empty(self):
        devices_str="{'devices':[]}"
        device_list=[]
        when(self.outer.rcms_cache).read_firstDevices_rcms(channel_code).thenReturn(devices_str)
        when(trans_outer_to_redis.rediscache).refresh_channel_devices(channel_code,False,device_list).thenReturn(device_list)
        device_list_act=self.outer.render_devices_rcms(channel_code,isNotFirst=False)
        self.assertEqual(device_list,device_list_act)

    def tearDown(self):
            unstub()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

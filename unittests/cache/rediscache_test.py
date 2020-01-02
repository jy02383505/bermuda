__author__ = 'root'
from __init__ import *
import core.redisfactory as redisfactory
when(redisfactory).RedisWrapper().thenReturn(mock())
from cache import rediscache

rediscache.portal_cache=mock()
rediscache.firstlayer_cache=mock()
rediscache.device_cache=mock()
rediscache.channels_cache=mock()
rediscache.COUNTER_CACHE=mock()
rediscache.BLACKLIST=mock()
rediscache.REWRITE_CACHE=mock()
rediscache.REGEXCONFIG =mock()
username='workercn'
channel_code='34567'
class RedisCachetest(unittest.TestCase):
    def setUp(self):
        when(redisfactory).getDB(6).thenReturn(mock())
        when(redisfactory).getDB(11).thenReturn(rediscache.firstlayer_cache )
        when(redisfactory).getDB(12).thenReturn(rediscache.device_cache)
        when(redisfactory).getDB(13).thenReturn(rediscache.channels_cache)

        when(redisfactory).getDB(4).thenReturn(rediscache.COUNTER_CACHE)
        when(redisfactory).getDB(1).thenReturn(rediscache.BLACKLIST)
        when(redisfactory).getDB(15).thenReturn(rediscache.REWRITE_CACHE)
        when(redisfactory).getDB(8).thenReturn(rediscache.REGEXCONFIG)
        # when(rediscache.device_cache.pipeline()).thenReturn(mock())

    def tearDown(self):
        unstub()

    def test_decrt_channel(self):
        channel_obj={'is_valid':True,'ignore_case':True}
        channel_obj_str = rediscache.derct_channel(channel_obj)
        self.assertEqual(channel_obj_str,json.JSONEncoder().encode(channel_obj))


    def test_refresh_user_channel(self):
        channels_arr=[{'name':'c1','is_valid':True,'ignore_case':True},{'name':'c2','is_valid':True,'ignore_case':True}]
        channels_map={}
        for channel in channels_arr:
            channel_utf8 = rediscache.derct_channel(channel)
            channels_map.setdefault(channel.get('name'),channel_utf8)
        when(rediscache.channels_cache).pipeline().thenReturn(mock())
        when(rediscache.channels_cache.pipeline()).delete(rediscache.CHANNELS_PREFIX % username).thenReturn("")
        when(rediscache.channels_cache.pipeline()).hmset(rediscache.CHANNELS_PREFIX % username,channels_map)
        channels_map_act=rediscache.refresh_user_channel(username,channels_arr)

        self.assertEqual(channels_map,channels_map_act)

    def test_refresh_channel_devices(self):
        devices_arr=[{'name':'c1','is_valid':True,'ignore_case':True},{'name':'c2','is_valid':True,'ignore_case':True}]
        devices_map={}
        for device in devices_arr:
            device_utf8 =json.JSONEncoder().encode(device)
            devices_map.setdefault(device.get('name'),device_utf8)
        # rediscache.device_cache = mock()
        when(rediscache.device_cache).pipeline().thenReturn(mock())
        when(rediscache.device_cache.pipeline()).delete(rediscache.DEVICES_PREFIX % channel_code).thenReturn("")
        when(rediscache.device_cache.pipeline()).hmset(rediscache.DEVICES_PREFIX % channel_code,devices_map)
        devices_map_act=rediscache.refresh_channel_devices(channel_code,True,devices_arr)

        self.assertEqual(devices_map,devices_map_act)
    def test_refresh_channel_firstdevices(self):
        devices_arr=[{'name':'c1','is_valid':True,'ignore_case':True},{'name':'c2','is_valid':True,'ignore_case':True}]
        devices_map={}
        for device in devices_arr:
            device_utf8 =json.JSONEncoder().encode(device)
            devices_map.setdefault(device.get('name'),device_utf8)
        when(rediscache.firstlayer_cache).pipeline().thenReturn(mock())
        when(rediscache.firstlayer_cache.pipeline()).delete(rediscache.FIRSTLAYER_DEVICES_PREFIX % channel_code).thenReturn("")
        when(rediscache.firstlayer_cache.pipeline()).hmset(rediscache.FIRSTLAYER_DEVICES_PREFIX % channel_code,devices_map)
        devices_map_act=rediscache.refresh_channel_devices(channel_code,False,devices_arr)

        self.assertEqual(devices_map,devices_map_act)
    def test_refresh_channels_portal(self):
        channels_arr=[{'channelName':'c1','is_valid':True,'ignore_case':True},{'channelName':'c2','is_valid':True,'ignore_case':True}]
        channels_map={}
        for device in channels_arr:
            device_utf8 =json.JSONEncoder().encode(device)
            channels_map.setdefault(device.get('channelName'),device_utf8)
        when(rediscache.portal_cache).pipeline().thenReturn(mock())
        when(rediscache.portal_cache.pipeline()).delete(rediscache.CHANNELS_PORTAL_PREFIX  % username).thenReturn("")
        when(rediscache.portal_cache.pipeline()).hmset(rediscache.CHANNELS_PORTAL_PREFIX  % username,channels_map)
        channels_map_act=rediscache.refresh_channels_portal(username,channels_arr)

        self.assertEqual(channels_map,channels_map_act)
    def test_refresh_customer_portal(self):
        channels_map={'k1':'v1','k2':'v2','k3':'v3'}
        when(rediscache.portal_cache).mset(channels_map)
        channels_map_act=rediscache.refresh_customer_portal(channels_map)
        verify(rediscache.portal_cache).mset(channels_map)
    def test_refresh_user_channel_portal(self):
        userinfo_str='{"user_key":"user_key"}'

        when(rediscache.portal_cache).set(rediscache.USERINFO_PORTAL_PREFIX % username,userinfo_str)
        userinfo_str_act = rediscache.refresh_user_channel_portal(username,userinfo_str)
        self.assertEqual(userinfo_str,userinfo_str_act)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()


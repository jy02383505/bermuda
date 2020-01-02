from __init__ import *
from core import rcmsapi
class Test(unittest.TestCase):

    def setUp(self):
        opened_url = mock()
        when(rcmsapi.urllib).urlopen(rcmsapi.CHANNELS_URL % 'chinacache', timeout= 10).thenReturn(opened_url)
        when(opened_url).read().thenReturn(json.dumps([{'code': '0005', 'name': 'http://www.chinacache.com', 'multilayer': False, 'customerCode': '3', 'billingCode': '0005', 'customerName': 'chinacache'}]))
        rcmsapi.redisutil.rediscache=mock()

        self.rediscache = rcmsapi.redisutil.rediscache
        self.rediscache.CHANNELS_PREFIX='c_by_%s'
        self.rediscache.DEVICES_PREFIX ='d_by_%s'
        self.rediscache.FIRSTLAYER_DEVICES_PREFIX='fd_by_%s'
        self.rediscache.USERNAME_LIST_KEY = 'usernames'
        self.rediscache.CHANNELS_BLACK = 'black_%s'
        # self.rediscache.read_from_redis = mock()
        self.username='chinacache'
        self.channel_code='52301'

        rcmsapi.redisutil.portal_cache=mock()
        rcmsapi.redisutil.firstlayer_cache=mock()
        rcmsapi.redisutil.device_cache=mock()
        rcmsapi.redisutil.channels_cache=mock()

        # rcmsapi.redisutil.trans_outer_to_redis=mock()
        # rcmsapi.redisutil.OutSysToRedis=mock()
        # chnl_rds=['{"name":"http://www.so.com/df/df"}','{"name":"http://www.duowan.com/df/df"}']
        # when(rcmsapi.redisutil.rediscache).read_from_redis(self.rediscache.USERNAME_LIST_KEY).thenReturn([self.username])
        # when(rcmsapi.redisutil.rediscache).read_from_redis(self.rediscache.CHANNELS_PREFIX, self.username).thenReturn(chnl_rds)
        when(rcmsapi.redisutil).MongoToRedis().thenReturn(mock())
        when(rcmsapi.redisutil).OutSysToRedis().thenReturn(mock())
    def tearDown(self):
        unstub()

    def test_isValidUrl_nocached(self):
        when(rcmsapi.redisutil.channels_cache).hget(self.rediscache.CHANNELS_PREFIX % self.username,'http://www.chinacache.com').thenReturn(None)
        when(rcmsapi.redisutil.channels_cache).hset().thenReturn(None)
        cc =[{"code": "7180", "customerName": "chinacache", "channelState": "COMMERCIAL", "multilayer": "false", "is_valid": "true", "name": "http://www.chinacache.com"}]
        when(rcmsapi.redisutil.OutSysToRedis()).render_channels_rcms(self.username).thenReturn(cc)
        when(rcmsapi.redisutil).getExtensiveDomainName().thenReturn('http://www.chinacache.com')
        self.assertTrue((True, False, '0005'), rcmsapi.isValidUrl('chinacache', 'http://www.chinacache.com/test.jpg'))
        # verify(rcmsapi.redisutil.channels_cache).hget(self.rediscache.CHANNELS_PREFIX % self.username,'http://www.chinacache.com')

    def test_isValidUrl_cached(self):
        channel = {'code': '0005', 'name': 'http://www.chinacache.com', 'multilayer': False, 'customerCode': '3', 'billingCode': '0005', 'customerName': 'chinacache', 'is_valid': True}
        when(rcmsapi.redisutil.channels_cache).hget(self.rediscache.CHANNELS_PREFIX % self.username,'http://www.chinacache.com').thenReturn(None)
        cc =[{"code": "7180", "customerName": "chinacache", "channelState": "COMMERCIAL", "multilayer": "false", "is_valid": "true", "name": "http://www.chinacache.com"}]
        when(rcmsapi.redisutil.OutSysToRedis()).render_channels_rcms(self.username).thenReturn(cc)
        when(rcmsapi.redisutil).getExtensiveDomainName().thenReturn('http://www.chinacache.com')
        self.assertTrue((True, False, '0005'), rcmsapi.isValidUrl('chinacache', 'http://www.chinacache.com/test.jpg'))
        # verify(rcmsapi.redisutil.channels_cache).hget(self.rediscache.CHANNELS_PREFIX % self.username,'http://www.chinacache.com')


    def test_isValidUrl_False(self):
        when(rcmsapi.redisutil.channels_cache).hget(self.rediscache.CHANNELS_PREFIX % self.username,'http://www.chinacache.com').thenReturn(None)
        when(rcmsapi.redisutil.channels_cache).expire().thenReturn(None)
        when(rcmsapi.redisutil.channels_cache).hget(self.rediscache.CHANNELS_PREFIX % self.username,'http://www.chinacache.com').thenReturn(None)
        cc =[{"code": "7180", "customerName": "chinacache", "channelState": "COMMERCIAL", "multilayer": "false", "is_valid": "true", "name": "http://www.chinacache.com"}]
        when(rcmsapi.redisutil.OutSysToRedis()).render_channels_rcms(self.username).thenReturn(cc)
        # verify(rcmsapi.redisutil.channels_cache).hset(self.rediscache.CHANNELS_BLACK%self.username,'http://www.chinacache.com',True)
        # verify(rcmsapi.redisutil.channels_cache).expire(self.rediscache.CHANNELS_BLACK % self.username, 300)
        when(rcmsapi.redisutil).getExtensiveDomainName().thenReturn('http://www.chinacache.com')
        self.assertTrue((False, False, 0), rcmsapi.isValidUrl('chinacache', 'http://www.wrong.com/test.jpg'))

    def test_get_channels(self):
        channels=[{u'name': u'http://www.so.com/df/df'}, {u'c': u'd'}]
        when(rcmsapi.redisutil.channels_cache).hvals(self.rediscache.CHANNELS_PREFIX % self.username).thenReturn(None)
        when(rcmsapi.redisutil.MongoToRedis()).render_channels_mongo(self.username).thenReturn(None)
        when(rcmsapi.redisutil.OutSysToRedis()).render_channels_rcms(self.username).thenReturn(None)
        chnl_rds=['{"name":"http://www.so.com/df/df"}','{"name":"http://www.duowan.com/df/df"}']
        # when(rcmsapi.redisutil.channels_cache).rpush(rcmsapi.redisutil.rediscache.USERNAME_LIST_KEY,self.username).thenReturn(chnl_rds)
        # when(rcmsapi.redisutil.channels_cache).hvals(rcmsapi.redisutil.rediscache.CHANNELS_PREFIX % self.username).thenReturn(chnl_rds)

        self.assertEqual(channels,rcmsapi.get_channels(self.username))
        verify(rcmsapi.redisutil.channels_cache,times(2)).hvals(self.rediscache.CHANNELS_PREFIX % self.username)
        # verify(rcmsapi.redisutil.MongoToRedis()).render_channels_mongo(self.username)
        # verify(rcmsapi.redisutil.OutSysToRedis).render_channels_rcms(self.username)
    def test_get_channels(self):
        channels=[{u'name': u'http://www.so.com/df/df'}, {u'name': u'http://www.duowan.com/df/df'}]
        when(rcmsapi.redisutil.channels_cache).hvals(self.rediscache.CHANNELS_PREFIX % self.username).thenReturn(None)
        when(rcmsapi.redisutil.MongoToRedis()).render_channels_mongo(self.username).thenReturn(None)
        when(rcmsapi.redisutil.OutSysToRedis()).render_channels_rcms(self.username).thenReturn(None)
        chnl_rds=['{"name":"http://www.so.com/df/df"}','{"name":"http://www.duowan.com/df/df"}']
        # when(rcmsapi.redisutil.channels_cache).rpush(rcmsapi.redisutil.rediscache.USERNAME_LIST_KEY,self.username).thenReturn(chnl_rds)
        when(rcmsapi.redisutil.channels_cache).hvals(rcmsapi.redisutil.rediscache.CHANNELS_PREFIX % self.username).thenReturn(chnl_rds)
        when(rcmsapi.redisutil.rediscache).read_from_redis(self.rediscache.USERNAME_LIST_KEY).thenReturn([self.username])
        when(rcmsapi.redisutil.rediscache).read_from_redis(self.rediscache.CHANNELS_PREFIX, self.username).thenReturn(chnl_rds)
        self.assertEqual(channels,rcmsapi.get_channels(self.username))
        # verify(rcmsapi.redisutil.channels_cache,times(1)).hvals(self.rediscache.CHANNELS_PREFIX % self.username)
        # verify(rcmsapi.redisutil.MongoToRedis()).render_channels_mongo(self.username)
        # verify(rcmsapi.redisutil.OutSysToRedis).render_channels_rcms(self.username)

    def test_getDevices(self):
        devs=[]
        when(rcmsapi.redisutil.device_cache).hvals(self.rediscache.DEVICES_PREFIX % self.channel_code).thenReturn(None)
        when(rcmsapi.redisutil.MongoToRedis()).render_devices_mongo(self.channel_code).thenReturn(None)
        when(rcmsapi.redisutil.OutSysToRedis()).render_devices_rcms(self.channel_code).thenReturn(None)
        self.assertEqual(devs,rcmsapi.getDevices(self.channel_code))
        # verify(rcmsapi.redisutil.device_cache,2).hvals(self.rediscache.DEVICES_PREFIX % self.channel_code)
        verify(rcmsapi.redisutil.MongoToRedis()).render_devices_mongo(self.channel_code)
        verify(rcmsapi.redisutil.OutSysToRedis()).render_devices_rcms(self.channel_code)

    def test_getFirstLayerDevices(self):
        devs=[]
        when(rcmsapi.redisutil.firstlayer_cache).hvals(self.rediscache.FIRSTLAYER_DEVICES_PREFIX % self.channel_code).thenReturn(None)
        when(rcmsapi.redisutil.MongoToRedis()).render_devices_mongo(self.channel_code,False).thenReturn(None)
        when(rcmsapi.redisutil.OutSysToRedis()).render_devices_rcms(self.channel_code,False).thenReturn(None)
        self.assertEqual(devs,rcmsapi.getFirstLayerDevices(self.channel_code))
        # verify(rcmsapi.redisutil.firstlayer_cache,2).hvals(self.rediscache.FIRSTLAYER_DEVICES_PREFIX % self.channel_code)
        verify(rcmsapi.redisutil.MongoToRedis()).render_devices_mongo(self.channel_code,False)
        verify(rcmsapi.redisutil.OutSysToRedis()).render_devices_rcms(self.channel_code,False)


    # def test_getDevStatus(self):
    #     unstub()
    #     self.assertEqual({'status': 'OPEN', 'name': 'CMN-JZ-1-3SA'}, rcmsapi.getDevStatus('CMN-JZ-1-3SA'))

if __name__ == "__main__":
    unittest.main()

__author__ = 'root'
# -*- coding:utf-8 -*-
import time
from __init__ import *
import simplejson as sjson
import urllib
from cache.api_rcms import ApiRCMS
import cache.api_rcms as apircms
ApiOuter=mock()

class ApiRCMSTest(unittest.TestCase):
    def setUp(self):

        self.username='workercn'
        self.channel_code='12345'
        self.rcms=ApiRCMS()
        self.com_rslt_list=[{"channelId": "410002206","code": "18505","name": "http://td.9wee.com","customerCode": "3351","customerName": "9wee","productCode": "9020100002079","channelState": "COMMERCIAL","transferTime": "2011-05-03 17:54:09.0","multilayer": "true"}]
        self.com_rslt='[xxx]'
        when(self.rcms).read_from_outer(apircms.All_CUSTOMERS).thenReturn(self.com_rslt)
        when(self.rcms).read_from_outer(apircms.ALL_CHANNELS ).thenReturn(self.com_rslt)
        when(self.rcms).read_from_outer(apircms.All_DEVICES).thenReturn(self.com_rslt)
        when(self.rcms).read_from_outer(apircms.ALL_FIRSTLAYER_DEVICES).thenReturn(self.com_rslt)
        when(self.rcms).read_from_outer(apircms.CUSTOMER_URL % urllib.quote(self.username)).thenReturn(self.com_rslt)
        when(self.rcms).read_from_outer(apircms.CUSTOMER_URL % urllib.quote(self.username)).thenReturn(self.com_rslt)
        when(self.rcms).read_from_outer(apircms.CHANNELS_URL % urllib.quote(self.username), need_retry=True).thenReturn(self.com_rslt)
        when(self.rcms).read_from_outer(apircms.DEVICES_URL % urllib.quote(self.channel_code), need_retry=True).thenReturn(self.com_rslt)
        when(self.rcms).read_from_outer(apircms.DEVICES_FIRSTLAYER_URL % urllib.quote(self.channel_code), need_retry=True).thenReturn(self.com_rslt)
        # when(self.rcms).read_from_outer(apircms.DEVICES_FIRSTLAYER_URL % urllib.quote(self.channel_code)).thenReturn(self.com_rslt)


    def test_read_allCustomers_rcms(self):
        self.assertEqual(self.rcms.read_allCustomers_rcms(),self.com_rslt)

    def test_read_allChannels_rcms(self):
        self.assertEqual(self.rcms.read_allChannels_rcms(),self.com_rslt)


    def test_read_allDevices_rcms(self):
        self.assertEqual(self.rcms.read_allDevices_rcms(),self.com_rslt)

    def test_read_allFirstLayer_Devices_rcms(self):
        self.assertEqual(self.rcms.read_allFirstLayer_Devices_rcms(),self.com_rslt)


    def test_read_userInfo_rcms(self):
        self.assertEqual(self.rcms.read_userInfo_rcms(self.username,times=1),self.com_rslt)

    def test_read_channels_rcms(self):
        com_rslt_s = '[{"channelId": "410002206","code": "18505","name": "http://td.9wee.com","customerCode": "3351","customerName": "9wee","productCode": "9020100002079","channelState": "COMMERCIAL","transferTime": "2011-05-03 17:54:09.0","multilayer": "true"}]'
        when(self.rcms).read_from_outer(apircms.CHANNELS_URL % urllib.quote(self.username), need_retry=True).thenReturn(com_rslt_s)
        self.assertEqual(self.rcms.read_channels_rcms(self.username,times=1),self.com_rslt_list)

    def test_read_devices_rcms(self):
         self.assertEqual(self.rcms.read_devices_rcms(self.channel_code,1),self.com_rslt)

    def test_read_firstDevices_rcms(self):
        self.assertEqual(self.rcms.read_firstDevices_rcms(self.channel_code, times=1),self.com_rslt)

    # def test_read_from_rcms(self):
    #     self.assertEqual(self.rcms.read_from_rcms(self.channel_code,times=1),self.com_rslt)

    def tearDown(self):
        unstub()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

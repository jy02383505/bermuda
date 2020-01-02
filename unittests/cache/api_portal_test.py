__author__ = 'root'
# -*- coding:utf-8 -*-
import unittest
from mockito import when, mock, unstub, verify,times
from cache.api_portal import ApiPortal
import cache.api_portal as apiportal
ApiOuter=mock()

class ApiPortalTest(unittest.TestCase):
    def setUp(self):

        self.username='workercn'
        self.portal=ApiPortal()
        when(self.portal).read_from_outer(apiportal.USERS_ROOT).thenReturn(apiportal.USERS_ROOT)
        when(self.portal).read_from_outer(apiportal.USERINFO_URL % self.username).thenReturn(apiportal.USERINFO_URL)
        when(self.portal).read_from_outer(apiportal.CHANNELS_URL % self.username).thenReturn(apiportal.CHANNELS_URL)



    def test_read_userInfo_portal(self):
        self.assertEqual(self.portal.read_userInfo_portal(self.username),apiportal.USERINFO_URL)

    def test_read_allCustomers_portal(self):
        self.assertEqual(self.portal.read_allCustomers_portal(),apiportal.USERS_ROOT)

    def test_read_channels_portal(self):
         self.assertEqual(self.portal.read_channels_portal(self.username),apiportal.CHANNELS_URL)
    def tearDown(self):
        unstub()
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
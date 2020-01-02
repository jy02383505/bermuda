__author__ = 'root'
# -*- coding:utf-8 -*-
import unittest
from mockito import when, mock, unstub, verify,times
from cache.api_outersys import ApiOuter
import cache.api_outersys as apiouter
import  urllib2



class ApiOuterTest(unittest.TestCase):
    def setUp(self):
        self.username='workercn'
        self.outer=ApiOuter()
        self.opened_url = mock()


    def test_read_from_outer(self):
        url='http://www.chiancache.com'
        when(apiouter.urllib2).urlopen(url,timeout=apiouter.TIMEOUT_OUTERURL).thenReturn(self.opened_url)
        str='[1,2,3]'
        when(self.opened_url).read().thenReturn(str)
        self.assertEqual(self.outer.read_from_outer(url,1),str)
    def test_read_from_outer_raise(self):
        # url='http://www.chiancache.com/su case'
        url_nospace='http://www.chiancache.com/sucase'
        when(apiouter.urllib2).urlopen(url_nospace,timeout=apiouter.TIMEOUT_OUTERURL).thenReturn(self.opened_url)
        when(self.opened_url).read().thenReturn(None)
        self.assertEqual(self.outer.read_from_outer(url=url_nospace,times=1),None)

        
    def test_is_diff_sort_cmp(self):
        devices_rcms=[{'name':'cx.x','link':'disp://dd.or.p'},{'name':'1cx.x','link':'1disp://dd.or.p'}]
        devices_mongo=[{'name':'cx.x','link':'disp://dd.or.p'},{'name':'1cx.x','link':'1disp://dd.or.p'}]
        self.assertFalse(self.outer.is_diff_sort_cmp(devices_rcms,devices_mongo))
        devices_mongo=[{'name':'cx.x','link':'disp://dd.or.p'},{'name1':'1cx.x','link':'1disp://dd.or.p'}]
        self.assertTrue(self.outer.is_diff_sort_cmp(devices_rcms,devices_mongo))
        devices_mongo=[{'name':'1cx.x','link':'1disp://dd.or.p'},{'name':'cx.x','link':'disp://dd.or.p'}]

        self.assertTrue(self.outer.is_diff_sort_cmp(devices_rcms,devices_mongo))

    def tearDown(self):
        unstub()
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
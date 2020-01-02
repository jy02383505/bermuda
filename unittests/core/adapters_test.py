#-*- coding:utf-8 -*-
from __init__ import *
when(redisfactory).getDB(2).thenReturn(mock())
from receiver import adapters

from werkzeug.exceptions import BadRequest, Forbidden

class Test(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.tencent_data = '''
        {
            "version": "1.0.0",
            "request_time": "2012-01-01 00:00:00",
            "serial_num": 123456,
            "update_urls": [
                "http://domain1.qq.com/folder1/file2.ext",
                "http://domain2.qq.com/folder1/file1.ext"
            ],
            "delete_urls": [
                "http://domain3.qq.com/folder5/sex.jpg"
            ],
            "verify": "bWQ1LmhleGRpZ2VzdCgp"
        }
        '''
        self.ntease_data = dict(
            username = '163',
            md5 = "temp_base_key",
            url_list = 'http://res.nie.netease.com/parker/js/clinic_filelist.js\r\nhttp://res.nie.netease.com/appbase/restaurant_filelist.js',
            dir_list = 'http://res.nie.netease.com/appbase/',
            item_id = '115')

        self.ntease_task = {"username":u"163", "urls":[u'http://res.nie.netease.com/parker/js/clinic_filelist.js', u'http://res.nie.netease.com/appbase/restaurant_filelist.js'], "dirs":[u'http://res.nie.netease.com/appbase/'], "callback":{"ntease_itemid":u'115'}}
        
        self.encrypt_data = '''
        {
            "username": "fanren",
            "urls": [
                "http://www.domain.com/folder1/file2.ext",
                "http://www.domain.com/folder1/file1.ext"
            ],
            "dirs": [
                "http://www.domain.com/folder1/"
            ],
            "verify": "6ded7a52636851da8ed84f7b7568487e"
        }
        '''
    def tearDown(self):
        unstub()
        unittest.TestCase.tearDown(self)


    # def test_get_tencent_task(self):
    #     when(adapters).is_verify_request_timeout(json.loads(self.tencent_data).get("request_time")).thenReturn(False)
    #     when(adapters).is_verify_tencent_failed(json.loads(self.tencent_data)).thenReturn(False)
    #     when(adapters.authentication).verify("qq", 'qq@tencent@11.11', None).thenReturn(True)
    #
    #     task, passed, message = adapters.get_tencent_task(self.tencent_data, '1.1.1.1')
    #     expected_task={'username': 'qq', 'update_urls': [u'http://domain1.qq.com/folder1/file2.ext', u'http://domain2.qq.com/folder1/file1.ext'], 'urls': [u'http://domain3.qq.com/folder5/sex.jpg']}
    #     self.assertEqual(expected_task, task)
    #     self.assertTrue(passed)
    #     self.assertEqual('{"ret": 0, "msg": ""}', message)


    def test_get_tencent_task_Forbidden(self):
        when(adapters).is_verify_request_timeout(json.loads(self.tencent_data).get("request_time")).thenReturn(False)
        when(adapters).is_verify_tencent_failed(json.loads(self.tencent_data)).thenReturn(False)
        remote_addr='1.1.1.1'
        when(adapters.authentication).verify(adapters.USERNAME_TENCENT, adapters.PASSWORD_KEY_TENCENT, remote_addr).thenRaise(Forbidden('Forbidden'))
        task, passed, message = adapters.get_tencent_task(self.tencent_data, remote_addr)

        self.assertEqual({"username":"qq", "urls":["http://domain3.qq.com/folder5/sex.jpg"], "update_urls":["http://domain1.qq.com/folder1/file2.ext", "http://domain2.qq.com/folder1/file1.ext"]}, task)
        self.assertFalse(passed)
        self.assertEqual(message, u'{"ret": -101, "msg": "未授权的上报IP:1.1.1.1"}')

    def test_get_tencent_task_BadRequest(self):
        self.assertRaises(BadRequest, adapters.get_tencent_task, '{a:"bb"}', '1.1.1.1')

    def test_is_verify_request_timeout(self):
        self.assertTrue(adapters.is_verify_request_timeout("2012-01-01 00:00:00"))
        when(adapters.time).time().thenReturn(1325347100.0)
        self.assertFalse(adapters.is_verify_request_timeout("2012-01-01 00:00:00"))

    def test_is_verify_tencent_failed(self):
        ori_task = json.loads(self.tencent_data)
        self.assertTrue(adapters.is_verify_tencent_failed(ori_task))
        ori_task["verify"] = 'Mzc2YmU4ZjQxYTk4MjMzNWVkY2Q4ZjBjMWJjNWM4N2U='
        self.assertFalse(adapters.is_verify_tencent_failed(ori_task))

    def test_get_ntease_task(self):
        when(adapters).is_verify_ntease_failed(self.ntease_data, None).thenReturn(False)
        self.assertEqual(adapters.get_ntease_task(self.ntease_data, None), (self.ntease_task, True, '<item_id>115</item_id><result>SUCCESS</result><detail>SUCCESS:Success</detail>'))

    def test_get_ntease_task_UserCheckFailed(self):
        when(adapters).is_verify_ntease_failed(self.ntease_data, None).thenReturn(True)
        self.assertEqual(adapters.get_ntease_task(self.ntease_data, None), (self.ntease_task, False, '<item_id>115</item_id><result>FAILURE</result><detail>ERROR:UserCheckFailed</detail>'))

    def test_get_ntease_task_IPForbidden(self):
        when(adapters).is_verify_ntease_failed(self.ntease_data, None).thenRaise(Forbidden('Forbidden'))
        self.assertEqual(adapters.get_ntease_task(self.ntease_data, None), (self.ntease_task, False, '<item_id>115</item_id><result>FAILURE</result><detail>ERROR:IPForbidden</detail>'))

    def test_is_verify_ntease_failed(self):
        when(adapters.authentication).verify('163', 'cc@ne.com', None).thenReturn(True)
        self.assertTrue(adapters.is_verify_ntease_failed(self.ntease_data, None))

        when(adapters.time).time().thenReturn(1325347100.0)
        when(adapters.time).strftime('%Y%m%d', 1325347100.0).thenReturn('20120319')

        self.ntease_data["md5"] = '508244bc3649134f78db1410386a04a9'
        self.assertFalse(adapters.is_verify_ntease_failed(self.ntease_data, None))

    def test_get_error_url(self):
        urls = ['http://www.a.aa/a.a', 'http://www.163.com/a.jpg', 'ahttp://www.163.com/a.jpg', 'http://www.chinacache.com/a.jpg']
        errorList = ['\nfollowing urls ignored because of bad format:\n', '\nahttp://www.163.com/a.jpg', '\nfollowing urls ignored because of domain range:\n', '\nhttp://www.chinacache.com/a.jpg', '\nfollowing urls ignored because of status code >= 404:\n', '\nhttp://www.a.aa/a.a']

        when(adapters).getHttpStatus('http://www.a.aa/a.a').thenReturn(404)
        when(adapters).getHttpStatus('http://www.163.com/a.jpg').thenReturn(200)
        when(adapters).getHttpStatus('http://www.chinacache.com/a.jpg').thenReturn(200)
        when(adapters.rcmsapi).isValidUrl('163', 'http://www.163.com/a.jpg').thenReturn((True, False, '0005'))
        when(adapters.rcmsapi).isValidUrl('163', 'http://www.chinacache.com/a.jpg').thenReturn((False, False, '0005'))
        self.assertEqual(adapters.get_error_url('163', urls), ''.join(errorList))

    def test_is_verify_encrypt_receiver_failed(self):
        when(adapters.time).gmtime().thenReturn(1325347100.0)
        when(adapters.time).strftime('%Y%m%d', 1325347100.0).thenReturn('20130106')
        when(adapters.time).gmtime().thenReturn(1325347100.0)
        self.assertFalse(adapters.is_verify_encrypt_receiver_failed(json.loads(self.encrypt_data)))

    def test_is_verify_encrypt_receiver_failed_error(self):
        when(adapters.time).gmtime().thenReturn(1325347100.0)
        when(adapters.time).strftime('%Y%m%d', 1325347100.0).thenReturn('2013')
        when(adapters.time).gmtime().thenReturn(1325347100.0)
        self.assertTrue(adapters.is_verify_encrypt_receiver_failed(json.loads(self.encrypt_data)))

    def test_is_verify_encrypt_search_failed(self):
        when(adapters.time).gmtime().thenReturn(1325347100.0)
        when(adapters.time).strftime('%Y%m%d', 1325347100.0).thenReturn('20130106')
        when(adapters.time).gmtime().thenReturn(1325347100.0)
        rid ="50d808a6cf4dc757a5a69aba"
        verify = '7d4e2e1d101e5d29920d6f193d5241f1'
        self.assertFalse(adapters.is_verify_encrypt_search_failed(rid,verify))

    def test_is_verify_encrypt_search_failed_error(self):
        when(adapters.time).gmtime().thenReturn(1325347100.0)
        when(adapters.time).strftime('%Y%m%d', 1325347100.0).thenReturn('20130106')
        when(adapters.time).gmtime().thenReturn(1325347100.0)
        rid ="50d808a6cf4dc757a5a69aba"
        verify = '7d4e2e1d101e5d29920d6f193d5241f124'
        self.assertTrue(adapters.is_verify_encrypt_search_failed(rid,verify))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testget_tencent_task']
    unittest.main()

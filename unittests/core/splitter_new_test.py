# -*- coding:utf-8 -*-

from __init__ import *
from core import splitter_new


mock_req_id="4e4c7b9f5bc89412ec000004"
def mock_insert(urls):
    for url in urls:
        url['_id'] = ObjectId(mock_req_id)


class SplitterTest(unittest.TestCase):

    def setUp(self):
        self.dt = datetime(2012, 1, 1, 0, 1, 0, 000000)
        self.db = mock()
        self.hour = time.strftime("%Y%m%d%H", time.localtime(time.time()))
        splitter_new.datetime = mock()
        splitter_new.redisfactory = mock()
        when(splitter_new.datetime).now().thenReturn(self.dt)
        when(splitter_new.database).db_session().thenReturn(self.db)
        splitter_new.REWRITE_CACHE = mock()
        splitter_new.COUNTER_CACHE = mock()
        splitter_new.rcmsapi=mock()
        when(bson).ObjectId().thenReturn(mock_req_id)

    def tearDown(self):
        unstub()

    def test_process_firstaccess(self):
        task = {"username": "chinacache", "urls": ["http://www.chinacache.com/a.jpg", "http://www.error.com/b.jpg"], "update_urls": ["http://www.chinacache.com/u.jpg"], "preload_urls": ["http://www.chinacache.com/c.jpg"], "dirs": ["http://www.chinacache.com/"], "callback": {"url": "http://callback"}}

        when(splitter_new.submit).delay(task).thenReturn(True)
        when(splitter_new.COUNTER_CACHE).get('%s_URL_chinacache' % self.hour).thenReturn(None)
        when(splitter_new.COUNTER_CACHE).get('%s_DIR_chinacache' % self.hour).thenReturn(None)
        self.db.request = mock()

        when(self.db.request).insert({"username": task.get("username"),
                                      "callback": task.get("callback"), "status": "PROGRESS",
                                      "created_time": self.dt, 'remote_addr': '', 'serial_num': ''}).thenReturn(ObjectId(mock_req_id))

        self.assertEqual({"r_id": mock_req_id}, splitter_new.process(self.db, task, True))
        # verify(splitter_new.submit).delay(task)

    def test_process_not_overload(self):
        task = {"username": "chinacache", "urls": ["http://www.chinacache.com/a.jpg", "http://www.error.com/b.jpg"], "update_urls": ["http://www.chinacache.com/u.jpg"], "preload_urls": ["http://www.chinacache.com/c.jpg"], "dirs": ["http://www.chinacache.com/"], "callback": {"url": "http://callback"}}

        when(splitter_new.submit).delay(task).thenReturn(True)
        when(splitter_new.COUNTER_CACHE).get('%s_URL_chinacache' % self.hour).thenReturn('-10')
        when(splitter_new.COUNTER_CACHE).get('%s_DIR_chinacache' % self.hour).thenReturn('-1')
        self.db.request = mock()

        when(self.db.request).insert({"username": task.get("username"),
                                      "callback": task.get("callback"), "status": "PROGRESS",
                                      "created_time": self.dt, 'remote_addr': '', 'serial_num': ''}).thenReturn(ObjectId(mock_req_id))

        self.assertEqual({"r_id": mock_req_id}, splitter_new.process(self.db, task, True))
        # verify(splitter_new.submit).delay(task)

    def test_process_overload(self):
        task = {"username": "chinacache", "urls": ["http://www.chinacache.com/a.jpg", "http://www.error.com/b.jpg"], "update_urls": ["http://www.chinacache.com/u.jpg"], "preload_urls": ["http://www.chinacache.com/c.jpg"], "dirs": ["http://www.chinacache.com/"], "callback": {"url": "http://callback"}}

        when(splitter_new.submit).delay(task).thenReturn(True)
        when(splitter_new.COUNTER_CACHE).get('%s_URL_chinacache' % self.hour).thenReturn('2')
        when(splitter_new.COUNTER_CACHE).get('%s_DIR_chinacache' % self.hour).thenReturn('1')

        when(splitter_new).setCounterCache('chinacache', 4, 'URL').thenReturn(None)
        when(splitter_new).setCounterCache('chinacache', 1, 'DIR').thenReturn(None)
        try:
            self.assertEqual({"urlExceed": 4, "dirExceed": 1}, splitter_new.process(self.db, task, True))
        except Exception,e:
            from werkzeug.exceptions import  InternalServerError
            self.assertTrue(isinstance(e,InternalServerError))

        # verify(splitter_new).setCounterCache('chinacache', 4, 'URL')
        # verify(splitter_new).setCounterCache('chinacache', 1, 'DIR')

    # def test_process_url_overload(self):
    #     task = {"username": "chinacache", "urls": ["http://www.chinacache.com/a.jpg", "http://www.error.com/b.jpg"], "update_urls": ["http://www.chinacache.com/u.jpg"], "preload_urls": ["http://www.chinacache.com/c.jpg"], "dirs": ["http://www.chinacache.com/"], "callback": {"url": "http://callback"}}
    #
    #     when(splitter_new.submit).delay(task).thenReturn(True)
    #     when(splitter_new.COUNTER_CACHE).get('%s_URL_chinacache' % self.hour).thenReturn('2')
    #     when(splitter_new.COUNTER_CACHE).get('%s_DIR_chinacache' % self.hour).thenReturn('-4')
    #     when(splitter_new).setCounterCache('chinacache', 4, 'URL').thenReturn(5)
    #
    #     self.db.request = mock()
    #     when(self.db.request).insert({"username": task.get("username"),
    #                                   "callback": task.get("callback"), "status": "PROGRESS",
    #                                   "created_time": self.dt, 'remote_addr': '', 'serial_num': ''}).thenReturn(ObjectId(mock_req_id))
    #
    #     self.assertEqual({"r_id": mock_req_id, 'urlExceed': 4}, splitter_new.process(self.db, task, True))
    #
    #     verify(splitter_new).setCounterCache('chinacache', 4, 'URL')
    #     task['urls'] = []
    #     task['update_urls'] = []
    #     verify(splitter_new.submit).delay(task)

    # def test_process_url_overload_without_dir(self):
    #     task = {"username": "chinacache", "urls": ["http://www.chinacache.com/a.jpg", "http://www.error.com/b.jpg"], "update_urls": ["http://www.chinacache.com/u.jpg"], "callback": {"url": "http://callback"}}
    #
    #     when(splitter_new.submit).delay(task).thenReturn(True)
    #     when(splitter_new.COUNTER_CACHE).get('%s_URL_chinacache' % self.hour).thenReturn('2')
    #     when(splitter_new.COUNTER_CACHE).get('%s_DIR_chinacache' % self.hour).thenReturn('-4')
    #     when(splitter_new).setCounterCache('chinacache', 3, 'URL').thenReturn(5)
    #
    #     self.assertEqual({'urlExceed': 3}, splitter_new.process(self.db, task, True))

    # def test_process_tencent(self):
    #     task = {"username": "chinacache",
    #             "urls": ["http://www.chinacache.com/a.jpg", "http://www.error.com/b.jpg"],
    #             "update_urls": ["http://www.chinacache.com/u.jpg"],
    #             "dirs": ["http://www.chinacache.com/"],
    #             "callback": {"url": "http://callback"},
    #             "remote_addr": "0.0.0.0",
    #             'serial_num': '123456',
    #             'request_time': '2012-01-01 01:01:01'}
    #
    #     when(splitter_new.COUNTER_CACHE).get('%s_URL_chinacache' % self.hour).thenReturn('-10')
    #     when(splitter_new.COUNTER_CACHE).get('%s_DIR_chinacache' % self.hour).thenReturn('-1')
    #
    #     when(splitter_new.datetime).strptime('2012-01-01 01:01:01', '%Y-%m-%d %X').thenReturn(datetime(2012, 1, 1, 1, 1, 1))
    #     when(splitter_new.submit).delay(task).thenReturn(True)
    #
    #     when(bson).ObjectId().thenReturn(ObjectId(mock_req_id))
    #
    #     self.assertEqual({"r_id": mock_req_id}, splitter_new.process(self.db, task))
    #     verify(splitter_new.submit).delay(task)

    # def test_submit(self):
    #     task = {"r_id": ObjectId(mock_req_id), "username": "chinacache", "urls": ["http://www.chinacache.com/a.jpg", "http://www.error.com/b.jpg"], "update_urls": ["http://www.chinacache.com/u.jpg"], "preload_urls": ["http://www.chinacache.com/c.jpg"], "dirs": ["http://www.chinacache.com/"], "callback": {"url": "http://callback"}}
    #     self.db.url = mock()
    #     self.db.request = mock()
    #     self.db.url.insert = mock_insert
    #     splitter_new.queue = mock()
    #     when(splitter_new.rcmsapi).isValidUrl('chinacache', "http://www.chinacache.com/a.jpg").thenReturn((True, False, '0005'))
    #     when(splitter_new.rcmsapi).isValidUrl('chinacache', "http://www.error.com/b.jpg").thenReturn((False, False, 0))
    #     when(splitter_new.rcmsapi).isValidUrl('chinacache', "http://www.chinacache.com/c.jpg").thenReturn((True, False, '0005'))
    #     when(splitter_new.rcmsapi).isValidUrl('chinacache', "http://www.chinacache.com/u.jpg").thenReturn((True, False, '0005'))
    #     when(splitter_new.rcmsapi).isValidUrl('chinacache', "http://www.chinacache.com/").thenReturn((True, False, '0005'))
    #     when(splitter_new.REWRITE_CACHE).exists("http://www.chinacache.com").thenReturn(False)
    #     splitter_new.COUNTER_CACHE = mock()
    #     when(splitter_new.COUNTER_CACHE).get('%s_URL_chinacache' % self.hour).thenReturn('-10')
    #     when(splitter_new.COUNTER_CACHE).get('%s_DIR_chinacache' % self.hour).thenReturn('-10')
    #     when(splitter_new).setCounterCache('chinacache', 4, 'URL').thenReturn(None)
    #     when(splitter_new).setCounterCache('chinacache', 1, 'URL').thenReturn(None)
    #
    #     when(splitter_new).noticeEmail(task).thenReturn(True)
    #
    #     urls = [{
    #             "r_id":ObjectId(mock_req_id),
    #             "url":"http://www.chinacache.com/a.jpg",
    #             "status":"PROGRESS",
    #             "isdir":False,
    #             "username":"chinacache",
    #             "action":"purge",
    #             "firstLayer":False,
    #             "channel_code":'0005'},
    #             {
    #             "r_id":ObjectId(mock_req_id),
    #             "url":"http://www.chinacache.com/",
    #             "status":"PROGRESS",
    #             "isdir":True,
    #             "username":"chinacache",
    #             "action":"expire",
    #             "firstLayer":False,
    #             "channel_code":'0005'},
    #             {
    #             "r_id":ObjectId(mock_req_id),
    #             "url":"http://www.chinacache.com/u.jpg",
    #             "status":"PROGRESS",
    #             "isdir":False,
    #     "username":"chinacache",
    #     "action":"expire",
    #     "firstLayer":False,
    #     "channel_code":'0005'},
    #     {
    #     "r_id":ObjectId(mock_req_id),
    #     "url":"http://www.chinacache.com/c.jpg",
    #     "status":"PROGRESS",
    #     "isdir":False,
    #     "username":"chinacache",
    #     "action":"preload",
    #     "firstLayer":False,
    #     "channel_code":'0005'}]
    #     url_list = [{
    #             "r_id":mock_req_id,
    #             "id":mock_req_id,
    #             "url":"http://www.chinacache.com/a.jpg",
    #             "status":"PROGRESS",
    #             "isdir":False,
    #             "username":"chinacache",
    #             "action":"purge",
    #             "firstLayer":False,
    #             "channel_code":'0005'},
    #             {
    #             "r_id":mock_req_id,
    #             "id":mock_req_id,
    #             "url":"http://www.chinacache.com/",
    #             "status":"PROGRESS",
    #             "isdir":True,
    #             "username":"chinacache",
    #             "action":"expire",
    #             "firstLayer":False,
    #             "channel_code":'0005'},
    #             {
    #             "r_id":mock_req_id,
    #             "id":mock_req_id,
    #             "url":"http://www.chinacache.com/u.jpg",
    #             "status":"PROGRESS",
    #             "isdir":False,
    #             "username":"chinacache",
    #             "action":"expire",
    #             "firstLayer":False,
    #             "channel_code":'0005'}, {
    #             "r_id":mock_req_id,
    #             "id":mock_req_id,
    #             "url":"http://www.chinacache.com/c.jpg",
    #             "status":"PROGRESS",
    #             "isdir":False,
    #             "username":"chinacache",
    #             "action":"preload",
    #             "firstLayer":False,
    #             "channel_code":'0005'}]
    #     splitter_new.submit(task,url_list)
    #     verify(self.db.url).insert(urls)
    #     verify(splitter_new.queue).put_json('url_queue', url_list)
    #     verify(self.db.request).update({"_id": ObjectId('4e4c7b9f5bc89412ec000004')}, {"$set": {"unprocess": 4}})
    #     verify(splitter_new).noticeEmail(task)
    #     verify(splitter_new).setCounterCache('chinacache', 4, 'URL')
    #     verify(splitter_new).setCounterCache('chinacache', 1, 'DIR')

    # def test_submit_sina(self):
    #     task = {"r_id": ObjectId(mock_req_id), "username": "sina_t", "urls": ["http://www.chinacache.com/a.jpg", "http://www.error.com/b.jpg"], "update_urls": ["http://www.chinacache.com/u.jpg"], "dirs": ["http://www.chinacache.com/"], "callback": {"url": "http://callback"}}
    #     self.db.url = mock()
    #     self.db.request = mock()
    #     self.db.url.insert = mock_insert
    #     splitter_new.queue = mock()
    #     when(splitter_new.rcmsapi).isValidUrl('sina_t', "http://www.chinacache.com/a.jpg").thenReturn((True, True, '0005'))
    #     when(splitter_new.rcmsapi).isValidUrl('sina_t', "http://www.error.com/b.jpg").thenReturn((False, True, 0))
    #     when(splitter_new.rcmsapi).isValidUrl('sina_t', "http://www.chinacache.com/u.jpg").thenReturn((True, True, '0005'))
    #     when(splitter_new.rcmsapi).isValidUrl('sina_t', "http://www.chinacache.com/").thenReturn((True, True, '0005'))
    #     splitter_new.redis_client = mock()
    #     when(splitter_new.REWRITE_CACHE).exists("http://www.chinacache.com").thenReturn(False)
    #     when(splitter_new).noticeEmail(task).thenReturn(True)
    #     when(splitter_new).setCounterCache('sina_t', 3, 'URL').thenReturn(None)
    #     when(splitter_new).setCounterCache('sina_t', 1, 'DIR').thenReturn(None)
    #
    #
    #     url_list = [{
    #             "r_id":mock_req_id,
    #             "id":mock_req_id,
    #             "url":"http://www.chinacache.com/a.jpg",
    #             "status":"PROGRESS",
    #             "isdir":False,
    #             "username":"sina_t",
    #             "action":"purge",
    #             "firstLayer":True,
    #             "channel_code":'0005',
    #             "threeLayer":True
    #             },
    #             {
    #             "r_id":mock_req_id,
    #             "id":mock_req_id,
    #             "url":"http://www.chinacache.com/",
    #             "status":"PROGRESS",
    #             "isdir":True,
    #             "username":"sina_t",
    #             "action":"expire",
    #             "firstLayer":True,
    #             "channel_code":'0005',
    #             "threeLayer":True},
    #             {
    #             "r_id":mock_req_id,
    #             "id":mock_req_id,
    #             "url":"http://www.chinacache.com/u.jpg",
    #             "status":"PROGRESS",
    #             "isdir":False,
    #             "username":"sina_t",
    #             "action":"expire",
    #             "firstLayer":True,
    #             "channel_code":'0005',
    #             "threeLayer":True}]
    #     splitter_new.submit(task,url_list)
    #     verify(splitter_new).setCounterCache('sina_t', 3, 'URL')
    #     verify(splitter_new).setCounterCache('sina_t', 1, 'DIR')
    #     verify(splitter_new.queue).put_json('url_queue', url_list)
    #     verify(self.db.request).update({"_id": ObjectId('4e4c7b9f5bc89412ec000004')}, {"$set": {"unprocess": 3}})
    #     verify(splitter_new).noticeEmail(task)

    # def test_submit_ntease(self):
    #     task = {"r_id": ObjectId(mock_req_id), "username": "163", "urls": ["http://www.chinacache.com/a.jpg"], "callback": {"ntease_itemid": '115'}}
    #     self.db.url = mock()
    #     self.db.request = mock()
    #     self.db.url.insert = mock_insert
    #     splitter_new.queue = mock()
    #     when(splitter_new.rcmsapi).isValidUrl('163', "http://www.chinacache.com/a.jpg").thenReturn((True, False, '0005'))
    #     splitter_new.redis_client = mock()
    #     when(splitter_new.REWRITE_CACHE).exists("http://www.chinacache.com").thenReturn(False)
    #     when(splitter_new).noticeEmail(task).thenReturn(True)
    #     when(splitter_new).setCounterCache('163', 1, 'URL').thenReturn(None)
    #     when(splitter_new).setCounterCache('163', 0, 'DIR').thenReturn(None)
    #     url_list = [{
    #             "r_id":mock_req_id,
    #             "id":mock_req_id,
    #             "url":"http://www.chinacache.com/a.jpg",
    #             "status":"PROGRESS",
    #             "isdir":False,
    #             "username":"163",
    #             "action":"purge",
    #             "firstLayer":False,
    #             "channel_code":'0005'}]
    #
    #     #when(splitter_new.verify_ntease_url).delay('163', url_list, '115').thenReturn(None)
    #     splitter_new.submit(task,url_list)
    #
    #     verify(splitter_new).setCounterCache('163', 1, 'URL')
    #     verify(splitter_new).setCounterCache('163', 0, 'DIR')
    #     verify(splitter_new.queue).put_json('url_queue', url_list)
    #     verify(self.db.request).update({"_id": ObjectId('4e4c7b9f5bc89412ec000004')}, {"$set": {"unprocess": 1}})
    #     verify(splitter_new).noticeEmail(task)
    #     #verify(splitter_new.verify_ntease_url).delay('163', url_list, '115')

    def test_getUrls_portal(self):
        username='chinacache'
        parent='chinacache'
        url="http://www.chinacache.com/test.jpg"
        task = {"r_id": ObjectId(mock_req_id), "username": "chinacache", "urls": [url], "dirs": ["0005", "http://www.chinacache.com/test.jpg"]}
        when(splitter_new.rcmsapi).getFirstLayerDevices('0005').thenReturn([])
        when(splitter_new.rcmsapi).isValidUrlByPortal(username, parent, url).thenReturn(True)
        when(splitter_new.rcmsapi).isValidUrl(parent, url).thenReturn(False)
        expected = [{
                "r_id":ObjectId(mock_req_id),
                'created_time': datetime(2012, 1, 1, 0, 1),
                "url":"http://www.chinacache.com/test.jpg",
                "status":"PROGRESS",
                "isdir":False,
                "username":"chinacache",
                "action":"purge",
                "is_multilayer":False,
                "channel_code":'0005'}
                ]
        expected=([],[])
        urls = splitter_new.getUrls(task)
        self.assertEqual(expected, urls)

    def test_getUrls_portal(self):
        username='chinacache'
        parent='chinacache'
        url="http://www.chinacache.com/test.jpg"
        task = {"isSub":True,"r_id": ObjectId(mock_req_id), "parent": "chinacache","username": "chinacache", "urls": [url], "dirs": ["0005", "http://www.chinacache.com/test.jpg"]}
        when(splitter_new.rcmsapi).getFirstLayerDevices('0005').thenReturn([])
        when(splitter_new.rcmsapi).isValidUrlByPortal(username, parent, url).thenReturn((True, True, 'channel_code', True))
        when(splitter_new.rcmsapi).isValidUrl(parent, url).thenReturn((True, True, 'channel_code', True))
        expected = ([{'status': 'PROGRESS', 'username': 'chinacache', 'ignore_case': True, 'parent': 'chinacache',
                      'is_multilayer': True, 'created_time': self.dt, 'channel_code': 'channel_code', 'isdir': False,
                      'url': 'http://www.chinacache.com/test.jpg', 'r_id': ObjectId(mock_req_id), 'action': 'purge',
                      '_id': mock_req_id}], [])

        urls = splitter_new.getUrls(task)

        self.assertEqual(expected, urls)

if __name__ == "__main__":
    unittest.main()


from __init__ import *
from core import splitter
mock_object_id='4e4c7b9f5bc89412ec000004'
def mock_insert(urls):
    for url in urls:
        url['_id'] = ObjectId(mock_object_id)


class SplitterTest(unittest.TestCase):

    def setUp(self):
        self.dt = datetime(2012, 1, 1, 0, 1, 0, 000000)
        self.db = mock()
        self.hour = time.strftime("%Y%m%d%H", time.localtime(time.time()))
        splitter.datetime = mock()
        splitter.redisfactory = mock()
        splitter.rcmsapi=mock()
        when(splitter.datetime).now().thenReturn(self.dt)
        when(splitter.database).db_session().thenReturn(self.db)
        splitter.REWRITE_CACHE = mock()
        splitter.COUNTER_CACHE = mock()
        splitter.bson=mock()
        when(splitter.bson).ObjectId().thenReturn(ObjectId("4e4c7b9f5bc89412ec000004"))

    def tearDown(self):
        unstub()

    def test_process_firstaccess(self):
        task = {"username": "chinacache", "urls": ["http://www.chinacache.com/a.jpg", "http://www.error.com/b.jpg"], "update_urls": ["http://www.chinacache.com/u.jpg"], "preload_urls": ["http://www.chinacache.com/c.jpg"], "dirs": ["http://www.chinacache.com/"], "callback": {"url": "http://callback"}}

        when(splitter.submit).delay(task).thenReturn(True)
        when(splitter.COUNTER_CACHE).get('%s_URL_chinacache' % self.hour).thenReturn(None)
        when(splitter.COUNTER_CACHE).get('%s_DIR_chinacache' % self.hour).thenReturn(None)
        self.db.request = mock()

        when(self.db.request).insert({"username": task.get("username"),
                                      "callback": task.get("callback"), "status": "PROGRESS",
                                      "created_time": self.dt, 'remote_addr': '', 'serial_num': ''}).thenReturn(ObjectId("4e4c7b9f5bc89412ec000004"))

        self.assertEqual({"r_id": "4e4c7b9f5bc89412ec000004"}, splitter.process(self.db, task, True))
        verify(splitter.submit).delay(task)

    def test_process_not_overload(self):
        task = {"username": "chinacache", "urls": ["http://www.chinacache.com/a.jpg", "http://www.error.com/b.jpg"], "update_urls": ["http://www.chinacache.com/u.jpg"], "preload_urls": ["http://www.chinacache.com/c.jpg"], "dirs": ["http://www.chinacache.com/"], "callback": {"url": "http://callback"}}

        when(splitter.submit).delay(task).thenReturn(True)
        when(splitter.COUNTER_CACHE).get('%s_URL_chinacache' % self.hour).thenReturn('-10')
        when(splitter.COUNTER_CACHE).get('%s_DIR_chinacache' % self.hour).thenReturn('-1')
        self.db.request = mock()

        when(self.db.request).insert({"username": task.get("username"),
                                      "callback": task.get("callback"), "status": "PROGRESS",
                                      "created_time": self.dt, 'remote_addr': '', 'serial_num': ''}).thenReturn(ObjectId("4e4c7b9f5bc89412ec000004"))

        self.assertEqual({"r_id": "4e4c7b9f5bc89412ec000004"}, splitter.process(self.db, task, True))
        verify(splitter.submit).delay(task)

    def test_process_overload(self):
        task = {"username": "chinacache", "urls": ["http://www.chinacache.com/a.jpg", "http://www.error.com/b.jpg"], "update_urls": ["http://www.chinacache.com/u.jpg"], "preload_urls": ["http://www.chinacache.com/c.jpg"], "dirs": ["http://www.chinacache.com/"], "callback": {"url": "http://callback"}}

        when(splitter.submit).delay(task).thenReturn(True)
        when(splitter.COUNTER_CACHE).get('%s_URL_chinacache' % self.hour).thenReturn('2')
        when(splitter.COUNTER_CACHE).get('%s_DIR_chinacache' % self.hour).thenReturn('1')
        task1 = {'username': 'chinacache', 'preload_urls': ['http://www.chinacache.com/c.jpg'], 'r_id': ObjectId(mock_object_id), 'update_urls': [], 'callback': {'url': 'http://callback'}, 'urls': [], 'dirs': ['http://www.chinacache.com/']}
        task2 = {'username': 'chinacache', 'preload_urls': ['http://www.chinacache.com/c.jpg'], 'r_id': ObjectId(mock_object_id), 'update_urls': [], 'callback': {'url': 'http://callback'}, 'urls': [], 'dirs': []}
        when(splitter).setCounterCache(task1, 3, 'URL').thenReturn(None)
        when(splitter).setCounterCache(task2, 1, 'DIR').thenReturn(None)

        self.assertEqual({'dirExceed': 1,"urlExceed": 3, 'r_id':mock_object_id}, splitter.process(self.db, task, True))
        # verify(splitter).setCounterCache(task1, 3, 'URL')
        # verify(splitter).setCounterCache(task2, 1, 'DIR')
        

    def test_process_url_overload(self):
        task = {"username": "chinacache", "urls": ["http://www.chinacache.com/a.jpg", "http://www.error.com/b.jpg"], "update_urls": ["http://www.chinacache.com/u.jpg"], "preload_urls": ["http://www.chinacache.com/c.jpg"], "dirs": ["http://www.chinacache.com/"], "callback": {"url": "http://callback"}}
        when(splitter.submit).delay(task).thenReturn(True)
        when(splitter.COUNTER_CACHE).get('%s_URL_chinacache' % self.hour).thenReturn('2')
        when(splitter.COUNTER_CACHE).get('%s_DIR_chinacache' % self.hour).thenReturn('-4')
        when(splitter).setCounterCache(task, 4, 'URL').thenReturn(5)

        self.db.request = mock()
        when(self.db.request).insert({"username": task.get("username"),
                                      "callback": task.get("callback"), "status": "PROGRESS",
                                      "created_time": self.dt, 'remote_addr': '', 'serial_num': ''}).thenReturn(ObjectId("4e4c7b9f5bc89412ec000004"))

        self.assertEqual({"r_id": "4e4c7b9f5bc89412ec000004", 'urlExceed': 3}, splitter.process(self.db, task, True))

        # verify(splitter).setCounterCache('chinacache', 4, 'URL')
        task['urls'] = []
        task['update_urls'] = []
        verify(splitter.submit).delay(task)

    def test_process_url_overload_without_dir(self):
        task = {"username": "chinacache", "urls": ["http://www.chinacache.com/a.jpg", "http://www.error.com/b.jpg"], "update_urls": ["http://www.chinacache.com/u.jpg"], "callback": {"url": "http://callback"}}

        when(splitter.submit).delay(task).thenReturn(True)
        when(splitter.COUNTER_CACHE).get('%s_URL_chinacache' % self.hour).thenReturn('2')
        when(splitter.COUNTER_CACHE).get('%s_DIR_chinacache' % self.hour).thenReturn('-4')
        when(splitter).setCounterCache('chinacache', 3, 'URL').thenReturn(5)

        self.assertEqual({'urlExceed': 3,'r_id': mock_object_id}, splitter.process(self.db, task, True))

    def test_process_tencent(self):
        task = {"username": "chinacache",
                "urls": ["http://www.chinacache.com/a.jpg", "http://www.error.com/b.jpg"],
                "update_urls": ["http://www.chinacache.com/u.jpg"],
                "dirs": ["http://www.chinacache.com/"],
                "callback": {"url": "http://callback"},
                "remote_addr": "0.0.0.0",
                'serial_num': '123456',
                'request_time': '2012-01-01 01:01:01'}

        when(splitter.COUNTER_CACHE).get('%s_URL_chinacache' % self.hour).thenReturn('-10')
        when(splitter.COUNTER_CACHE).get('%s_DIR_chinacache' % self.hour).thenReturn('-1')

        when(splitter.datetime).strptime('2012-01-01 01:01:01', '%Y-%m-%d %X').thenReturn(datetime(2012, 1, 1, 1, 1, 1))
        when(splitter.submit).delay(task).thenReturn(True)

        when(bson).ObjectId().thenReturn(ObjectId("4e4c7b9f5bc89412ec000004"))

        self.assertEqual({"r_id": "4e4c7b9f5bc89412ec000004"}, splitter.process(self.db, task))
        verify(splitter.submit).delay(task)


    def test_submit(self):
        task = {"r_id": ObjectId("4e4c7b9f5bc89412ec000004"), "username": "chinacache", "urls": ["http://www.chinacache.com/a.jpg", "http://www.error.com/b.jpg"], "update_urls": ["http://www.chinacache.com/u.jpg"], "preload_urls": ["http://www.chinacache.com/c.jpg"], "dirs": ["http://www.chinacache.com/"], "callback": {"url": "http://callback"}}
        self.db.url = mock()
        self.db.request = mock()
        self.db.url.insert = mock_insert
        splitter.queue = mock()
        when(splitter.rcmsapi).isValidUrl('chinacache', "http://www.chinacache.com/a.jpg").thenReturn((True, False, '0005'))
        when(splitter.rcmsapi).isValidUrl('chinacache', "http://www.error.com/b.jpg").thenReturn((False, False, 0))
        when(splitter.rcmsapi).isValidUrl('chinacache', "http://www.chinacache.com/c.jpg").thenReturn((True, False, '0005'))
        when(splitter.rcmsapi).isValidUrl('chinacache', "http://www.chinacache.com/u.jpg").thenReturn((True, False, '0005'))
        when(splitter.rcmsapi).isValidUrl('chinacache', "http://www.chinacache.com/").thenReturn((True, False, '0005'))
        when(splitter.REWRITE_CACHE).exists("http://www.chinacache.com").thenReturn(False)
        splitter.COUNTER_CACHE = mock()
        when(splitter.COUNTER_CACHE).get('%s_URL_chinacache' % self.hour).thenReturn('-10')
        when(splitter.COUNTER_CACHE).get('%s_DIR_chinacache' % self.hour).thenReturn('-10')
        when(splitter).setCounterCache('chinacache', 4, 'URL').thenReturn(None)
        when(splitter).setCounterCache('chinacache', 1, 'URL').thenReturn(None)

        when(splitter).noticeEmail(task).thenReturn(True)

        splitter.submit(task)
        urls = [{
                "r_id":ObjectId("4e4c7b9f5bc89412ec000004"),
                "url":"http://www.chinacache.com/a.jpg",
                "status":"PROGRESS",
                "isdir":False,
                "username":"chinacache",
                "action":"purge",
                "firstLayer":False,
                "channel_code":'0005'},
                {
                "r_id":ObjectId("4e4c7b9f5bc89412ec000004"),
                "url":"http://www.chinacache.com/",
                "status":"PROGRESS",
                "isdir":True,
                "username":"chinacache",
                "action":"expire",
                "firstLayer":False,
                "channel_code":'0005'},
                {
                "r_id":ObjectId("4e4c7b9f5bc89412ec000004"),
                "url":"http://www.chinacache.com/u.jpg",
                "status":"PROGRESS",
                "isdir":False,
        "username":"chinacache",
        "action":"expire",
        "firstLayer":False,
        "channel_code":'0005'},
        {
        "r_id":ObjectId("4e4c7b9f5bc89412ec000004"),
        "url":"http://www.chinacache.com/c.jpg",
        "status":"PROGRESS",
        "isdir":False,
        "username":"chinacache",
        "action":"preload",
        "firstLayer":False,
        "channel_code":'0005'}]
        url_list = [{
                "r_id":"4e4c7b9f5bc89412ec000004",
                "id":"4e4c7b9f5bc89412ec000004",
                "url":"http://www.chinacache.com/a.jpg",
                "status":"PROGRESS",
                "isdir":False,
                "username":"chinacache",
                "action":"purge",
                "firstLayer":False,
                "channel_code":'0005'},
                {
                "r_id":"4e4c7b9f5bc89412ec000004",
                "id":"4e4c7b9f5bc89412ec000004",
                "url":"http://www.chinacache.com/",
                "status":"PROGRESS",
                "isdir":True,
                "username":"chinacache",
                "action":"expire",
                "firstLayer":False,
                "channel_code":'0005'},
                {
                "r_id":"4e4c7b9f5bc89412ec000004",
                "id":"4e4c7b9f5bc89412ec000004",
                "url":"http://www.chinacache.com/u.jpg",
                "status":"PROGRESS",
                "isdir":False,
                "username":"chinacache",
                "action":"expire",
                "firstLayer":False,
                "channel_code":'0005'}, {
                "r_id":"4e4c7b9f5bc89412ec000004",
                "id":"4e4c7b9f5bc89412ec000004",
                "url":"http://www.chinacache.com/c.jpg",
                "status":"PROGRESS",
                "isdir":False,
                "username":"chinacache",
                "action":"preload",
                "firstLayer":False,
                "channel_code":'0005'}]
        verify(self.db.url).insert(urls)
        # verify(splitter.queue).put_json('url_queue', url_list)
        # verify(self.db.request).update({"_id": ObjectId(mock_object_id)}, {"$set": {"unprocess": 4}})
        # verify(splitter).noticeEmail(task)
        # verify(splitter).setCounterCache('chinacache', 4, 'URL')
        # verify(splitter).setCounterCache('chinacache', 1, 'DIR')
    #
    def test_submit_sina(self):
        task = {"r_id": ObjectId("4e4c7b9f5bc89412ec000004"), "username": "sina_t", "urls": ["http://www.chinacache.com/a.jpg", "http://www.error.com/b.jpg"], "update_urls": ["http://www.chinacache.com/u.jpg"], "dirs": ["http://www.chinacache.com/"], "callback": {"url": "http://callback"}}
        self.db.url = mock()
        self.db.request = mock()
        self.db.url.insert = mock_insert
        splitter.queue = mock()
        when(splitter.rcmsapi).isValidUrl('sina_t', "http://www.chinacache.com/a.jpg").thenReturn((True, True, '0005'))
        when(splitter.rcmsapi).isValidUrl('sina_t', "http://www.error.com/b.jpg").thenReturn((False, True, 0))
        when(splitter.rcmsapi).isValidUrl('sina_t', "http://www.chinacache.com/u.jpg").thenReturn((True, True, '0005'))
        when(splitter.rcmsapi).isValidUrl('sina_t', "http://www.chinacache.com/").thenReturn((True, True, '0005'))
        splitter.redis_client = mock()
        when(splitter.REWRITE_CACHE).exists("http://www.chinacache.com").thenReturn(False)
        when(splitter).noticeEmail(task).thenReturn(True)
        when(splitter).setCounterCache('sina_t', 3, 'URL').thenReturn(None)
        when(splitter).setCounterCache('sina_t', 1, 'DIR').thenReturn(None)

        splitter.submit(task)

        url_list = [{
                "r_id":"4e4c7b9f5bc89412ec000004",
                "id":"4e4c7b9f5bc89412ec000004",
                "url":"http://www.chinacache.com/a.jpg",
                "status":"PROGRESS",
                "isdir":False,
                "username":"sina_t",
                "action":"purge",
                "firstLayer":True,
                "channel_code":'0005',
                "threeLayer":True
                },
                {
                "r_id":"4e4c7b9f5bc89412ec000004",
                "id":"4e4c7b9f5bc89412ec000004",
                "url":"http://www.chinacache.com/",
                "status":"PROGRESS",
                "isdir":True,
                "username":"sina_t",
                "action":"expire",
                "firstLayer":True,
                "channel_code":'0005',
                "threeLayer":True},
                {
                "r_id":"4e4c7b9f5bc89412ec000004",
                "id":"4e4c7b9f5bc89412ec000004",
                "url":"http://www.chinacache.com/u.jpg",
                "status":"PROGRESS",
                "isdir":False,
                "username":"sina_t",
                "action":"expire",
                "firstLayer":True,
                "channel_code":'0005',
                "threeLayer":True}]

    #     verify(splitter).setCounterCache('sina_t', 3, 'URL')
    #     verify(splitter).setCounterCache('sina_t', 1, 'DIR')
    #     verify(splitter.queue).put_json('url_queue', url_list)
    #     verify(self.db.request).update({"_id": ObjectId(mock_object_id)}, {"$set": {"unprocess": 3}})
    #     verify(splitter).noticeEmail(task)
    #
    def test_submit_ntease(self):
        task = {"r_id": ObjectId("4e4c7b9f5bc89412ec000004"), "username": "163", "urls": ["http://www.chinacache.com/a.jpg"], "callback": {"ntease_itemid": '115'}}
        self.db.url = mock()
        self.db.request = mock()
        self.db.url.insert = mock_insert
        splitter.queue = mock()
        when(splitter.rcmsapi).isValidUrl('163', "http://www.chinacache.com/a.jpg").thenReturn((True, False, '0005'))
        splitter.redis_client = mock()
        when(splitter.REWRITE_CACHE).exists("http://www.chinacache.com").thenReturn(False)
        when(splitter).noticeEmail(task).thenReturn(True)
        when(splitter).setCounterCache('163', 1, 'URL').thenReturn(None)
        when(splitter).setCounterCache('163', 0, 'DIR').thenReturn(None)
        url_list = [{
                "r_id":"4e4c7b9f5bc89412ec000004",
                "id":"4e4c7b9f5bc89412ec000004",
                "url":"http://www.chinacache.com/a.jpg",
                "status":"PROGRESS",
                "isdir":False,
                "username":"163",
                "action":"purge",
                "firstLayer":False,
                "channel_code":'0005'}]

        # when(splitter.verify_ntease_url).delay('163', url_list, '115').thenReturn(None)
        splitter.submit(task)
    #
    #     verify(splitter).setCounterCache('163', 1, 'URL')
    #     verify(splitter).setCounterCache('163', 0, 'DIR')
    #     verify(splitter.queue).put_json('url_queue', url_list)
    #     verify(self.db.request).update({"_id": ObjectId(mock_object_id)}, {"$set": {"unprocess": 1}})
    #     verify(splitter).noticeEmail(task)
    #     #verify(splitter.verify_ntease_url).delay('163', url_list, '115')

    def test_getUrls_portal(self):
        task = {"r_id": ObjectId(mock_object_id),"dirs":["http://www.sh.com"], "username": "chinacache","urls":["http://www.chinacache.com/test.jpg"], "portalurls": [["0005", "http://www.chinacache.com/test.jpg"]], "portaldirs": []}
        when(splitter.rcmsapi).isValidUrl("chinacache",task.get('urls')[0]).thenReturn([True, False, '0005', True])
        urls = splitter.getUrls(task)
        expected = [{'status': 'PROGRESS', 'username': 'chinacache',
                     'ignore_case': True, 'parent': 'chinacache',
                     'is_multilayer': False,
                     'created_time': self.dt,
                     'channel_code': '0005',
                     'isdir': False,
                     'url': 'http://www.chinacache.com/test.jpg',
                     'r_id': ObjectId(mock_object_id), 'action': 'purge'}]

        self.assertEqual(expected, urls)

    def test_setCounterCache(self):
        refresh_task={'username':'workercn','URL_OVERLOAD_PER_HOUR':1,"DIR_OVERLOAD_PER_HOUR":1}
        refresh_type='url'
        count=2
        now = time.time()
        when(time).time().thenReturn(now)

        key='xx'
        pipe_mock=Basesplitter()
        when(splitter).getUserKey('workercn', refresh_type).thenReturn(key)
        when(splitter.COUNTER_CACHE).pipeline().thenReturn(pipe_mock)


        splitter.setCounterCache(refresh_task, count, refresh_type)

class Basesplitter(object):
    def __init__(self):
        pass
    def __enter__(self):
        return pipe_mock()
        pass
    def pipeline(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

class pipe_mock():
    def watch(self,key):
        pass
    def multi(self):
        pass
    def get(self,key):
        return 2
    def set(self,key, value):
        pass
    def expire(self,key, value):
        pass

    def execute(self):
        pass

if __name__ == "__main__":
    unittest.main()

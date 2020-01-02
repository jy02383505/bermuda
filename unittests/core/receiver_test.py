# -*- coding:utf-8 -*-
from __init__ import *
# import pymongo
# when(ReplicaSetConnection().thenReturn(mock())
when(database).db_session().thenReturn(mock())
from receiver import receiver

from werkzeug.exceptions import Forbidden
from werkzeug.datastructures import ImmutableMultiDict


class ReceiverTest(unittest.TestCase):

    def setUp(self):
        self.db = mock()

        self.app = receiver.create_app(self.db, self.db).test_client()
        receiver.user_cache = mock()
        self.urls = [{u'isdir': False,
                    u'status': u'FINISHED',
                    u'is_multilayer': True,
                    u'username': u'chinacache',
                    u'created_time': datetime(2012, 1, 1, 0, 0, 0, 000000),
                    u'url': u'http://www.chinacache.com/test.jpg',
                    u'finish_time': datetime(2012, 1, 1, 0, 1, 0, 000000),
                    u'r_id': ObjectId('4e79a53c815c5e25fe001227'),
                    u'action': u'purge',
                    u'_id': ObjectId('4e79a53c815c5e25fe001228'),
                    u'channel_code': u'0005'}
            ]
        self.refresh_request = [{
            "_id": ObjectId("4e79a53c815c5e25fe001227"),
            "callback": None,
            "created_time": datetime(2012, 1, 1, 0, 0, 0, 000000),
            "finish_time": datetime(2012, 1, 1, 0, 1, 0, 000000),
            "status": "FINISHED",
            "username": "chinacache"
        }, {
            "_id": ObjectId("4e79a53c815c5e25fe001228"),
            "callback": None,
            "created_time": datetime(2012, 1, 1, 0, 0, 0, 000000),
            "finish_time": datetime(2012, 1, 1, 0, 1, 0, 000000),
            "status": "FINISHED",
            "username": "chinacache"
        }]

    def tearDown(self):
        unstub()
        unittest.TestCase.tearDown(self)

    # def test_post_request(self):
    #     task = json.loads('{"username":"chinacache","URL_OVERLOAD_PER_HOUR":40,"DIR_OVERLOAD_PER_HOUR":40,"urls":["http://www.chinacache.com/test.jpg"]}')
    #     task["remote_addr"] = None
    #     when(receiver.splitter).process(self.db, task, True).thenReturn({'r_id': '4e79a53c815c5e25fe001227'})
    #     ticket={"name": "chinacache", "pass": True,"isSub":True,"parent":True,"URL_OVERLOAD_PER_HOUR":40,"DIR_OVERLOAD_PER_HOUR":40}
    #     when(receiver.authentication).verify("chinacache", "chinacache", None).thenReturn(ticket)
    #     # rv={'status_code':200,'data':'{"r_id": "4e79a53c815c5e25fe001227"}'}
    #     rv= self.app.post('/content/refresh', data=dict(username = 'chinacache', password = 'chinacache', task = '{"urls":["http://www.chinacache.com/test.jpg"]}'))
    #     self.assertEqual(200, rv.status_code)
    #     self.assertEqual({'r_id': '4e79a53c815c5e25fe001227'}, json.loads(rv.data))

    def test_post_request_errortask(self):
        # rv={'status_code':400,'data':"The schema of task is error."}
        rv=self.app.post('/content/refresh', data=dict(username = 'chinacache', password = 'chinacache', task = '{urls:["http://www.chinacache.com/test.jpg"]}'))
        assert 400 == rv.status_code
        assert "The schema of task is error." in rv.data

    def test_post_request_errorpassword(self):
        when(receiver.authentication).verify("chinacache", "wrongpassword", None).thenRaise(Forbidden("WRONG_PASSWORD"))
        rv={'status_code':403,'data':'WRONG_PASSWORD'}
        rv=self.app.post('/content/refresh', data=dict(username = 'chinacache', password = 'wrongpassword', task = '{"urls":["http://www.chinacache.com/test.jpg"]}'))

        assert 403 == rv.status_code
        assert 'WRONG_PASSWORD' in rv.data

    def test_post_request_internalerror(self):
        when(receiver.authentication).verify("chinacache", "chinacache", None).thenRaise(Exception("hi there!"))
        rv = self.app.post('/content/refresh', data=dict(username = 'chinacache', password = 'chinacache', task = '{"urls":["http://www.chinacache.com/test.jpg"]}'))
        self.assertEqual(500, rv.status_code)
        self.assertEqual('Internal Server Error.', rv.data)

    def test_post_request_formnull(self):
        when(receiver.authentication).verify("chinacache", "chinacache", None).thenRaise(Exception("hi there!"))
        data_dict=dict(username = 'chinacache', password = 'chinacache', task = '{"urls":["http://www.chinacache.com/test.jpg"]}')
        data_str=json.dumps(data_dict)
        rv = self.app.post('/content/refresh', data=data_str,headers={'content-type': 'application/json'})
        # ,headers={'content-type': 'application/json'})
        self.assertEqual(500, rv.status_code)
        self.assertEqual('Internal Server Error.', rv.data)

    # def test_search_unknown(self):
    #     when(receiver.authentication).verify("chinacache", "chinacache", None).thenReturn({"name": "chinacache", "pass": True})
    #     db3 = mock()
    #     # when(receiver.redisfactory).getDB(3).thenReturn(db3)
    #     when(db3).get("chinacache4e79a53c815c5e25fe001227").thenReturn(None)
    #     receiver.datetime = mock()
    #     when(receiver.datetime).now().thenReturn(datetime(2012, 1, 1, 0, 1, 0, 000000))
    #     self.db.request = mock()
    #     refresh_request = {
    #                         "_id": ObjectId("4e79a53c815c5e25fe001227"),
    #                         "callback": None,
    #                         "created_time": datetime(2012, 1, 1, 0, 0, 0, 000000),
    #                         "status": "PROGRESS",
    #                         "username": "chinacache"
    #                     }
    #     when(self.db.request).find_one({'username': 'chinacache', '_id': ObjectId('4e79a53c815c5e25fe001227')}).thenReturn(refresh_request)
    #     self.db.url = mock()
    #     urls = [{u'isdir': False,
    #             u'status': u'FINISHED',
    #             u'is_multilayer': True,
    #             u'username': u'chinacache',
    #             u'created_time': datetime(2012, 1, 1, 0, 0, 4, 460000),
    #             u'url': u'http://www.chinacache.com/test.jpg',
    #             u'finish_time': datetime(2012, 1, 1, 0, 0, 7, 947000),
    #             u'r_id': ObjectId('4e79a53c815c5e25fe001227'),
    #             u'action': u'purge',
    #             u'_id': ObjectId('4e79a53c815c5e25fe001228'),
    #             u'channel_code': u'0005'},
    #             {u'isdir': False,
    #             u'status': u'PROGRESS',
    #             u'is_multilayer': True,
    #             u'username': u'chinacache',
    #             u'created_time': datetime(2012, 1, 1, 0, 0, 4, 460000),
    #             u'url': u'http://www.chinacache.com/test2.jpg',
    #             u'finish_time': None,
    #             u'r_id': ObjectId('4e79a53c815c5e25fe001227'),
    #             u'action': u'purge',
    #             u'_id': ObjectId('4e79a53c815c5e25fe001229'),
    #             u'channel_code': u'0005'}]
    #     when(self.db.url).find({'r_id': ObjectId('4e79a53c815c5e25fe001227')}).thenReturn(urls)
    #     expected = '''{
    #                     "r_id":"4e79a53c815c5e25fe001227",
    #                     "status":"UNKNOWN",
    #                     "createdTime":"2012-01-01 00:00:00",
    #                     "finishedTime":null,
    #                     "successRate":0.5,
    #                     "totalTime":60,
    #                     "username":"chinacache",
    #                     "urlStatus":[
    #                         {"url":"http://www.chinacache.com/test.jpg","code":200},
    #                         {"url":"http://www.chinacache.com/test2.jpg","code":0}
    #                     ]
    #                 }'''
    #     # rv={'status_code':200,'data':expected}
    #     rv=self.app.get('/content/refresh/4e79a53c815c5e25fe001227?username=chinacache&password=chinacache')
    #
    #     self.assertEqual(200, rv.status_code)
    #
    #     self.assertEqual(json.loads(expected), json.loads(rv.data))

    # def test_search_success(self):
    #     when(receiver.authentication).verify("chinacache", "chinacache", None).thenReturn({"name": "chinacache", "pass": True})
    #     db3 = mock()
    #     # when(receiver.redisfactory).getDB(3).thenReturn(db3)
    #     when(db3).get("chinacache4e79a53c815c5e25fe001227").thenReturn(None)
    #     self.db.request = mock()
    #     refresh_request = {
    #                         "_id": ObjectId("4e79a53c815c5e25fe001227"),
    #                         "callback": None,
    #                         "created_time": datetime(2012, 1, 1, 0, 0, 0, 000000),
    #                         "finish_time": datetime(2012, 1, 1, 0, 1, 0, 000000),
    #                         "status": "FINISHED",
    #                         "username": "chinacache"
    #                     }
    #     when(self.db.request).find_one({'username': 'chinacache', '_id': ObjectId('4e79a53c815c5e25fe001227')}).thenReturn(refresh_request)
    #     self.db.url = mock()
    #     when(self.db.url).find({'r_id': ObjectId('4e79a53c815c5e25fe001227')}).thenReturn(self.urls)
    #
    #     expected = json.loads('''{
    #                 "status":"SUCCESS",
    #                 "finishedTime":"2012-01-01 00:01:00",
    #                 "successRate":1,
    #                 "totalTime":60,
    #                 "r_id":"4e79a53c815c5e25fe001227",
    #                 "createdTime":"2012-01-01 00:00:00",
    #                 "username":"chinacache",
    #                 "urlStatus":[
    #                     {"url":"http://www.chinacache.com/test.jpg","code":200}
    #                 ]
    #             }''')
    #     # rv={'status_code':200,'data':expected}
    #     rv=self.app.get('/content/refresh/4e79a53c815c5e25fe001227?username=chinacache&password=chinacache')
    #     self.assertEqual(200, rv.status_code)
    #     self.assertEqual(expected, rv.data)
        # verify(db3).set("chinacache4e79a53c815c5e25fe001227", '{"status": "SUCCESS", "finishedTime": "2012-01-01 00:01:00", "successRate": 1, "totalTime": 60, "r_id": "4e79a53c815c5e25fe001227", "createdTime": "2012-01-01 00:00:00", "username": "chinacache", "urlStatus": [{"url": "http://www.chinacache.com/test.jpg", "code": 200}]}')
        # verify(db3).expire("chinacache4e79a53c815c5e25fe001227", 300)

    # def test_search_success_cached(self):
    #     expected = '''{
    #                     "r_id":"4e79a53c815c5e25fe001227",
    #                     "status":"SUCCESS",
    #                     "createdTime":"2012-01-01 00:00:00",
    #                     "finishedTime":"2012-01-01 00:01:00",
    #                     "successRate":1,
    #                     "totalTime":60,
    #                     "username":"chinacache",
    #                     "urlStatus":[
    #                         {"url":"http://www.chinacache.com/test.jpg","code":200}
    #                     ]
    #                 }'''
    #     when(receiver.authentication).verify("chinacache", "chinacache", None).thenReturn({"name": "chinacache", "pass": True})
    #     db3 = mock()
    #     # when(receiver.redisfactory).getDB(3).thenReturn(db3);
    #     when(db3).get("chinacache4e79a53c815c5e25fe001227").thenReturn(expected)
    #     rv={'status_code':200,'data':expected}
    #     self.app.get('/content/refresh/4e79a53c815c5e25fe001227?username=chinacache&password=chinacache')
    #
    #     self.assertEqual(200, rv.status_code)
    #     self.assertEqual(json.loads(expected), json.loads(rv.data))

    # def test_search_notfound(self):
    #     when(receiver.authentication).verify("chinacache", "chinacache", None).thenReturn({"name": "chinacache", "pass": True})
    #     db3 = mock()
    #     # when(receiver.redisfactory).getDB(3).thenReturn(db3);
    #     when(db3).get("chinacache4e79a53c815c5e25fe001227").thenReturn(None)
    #     self.db.request = mock()
    #     when(self.db.request).find_one({'username': 'chinacache', '_id': ObjectId('4e79a53c815c5e25fe001227')}).thenReturn(None)
    #     expected='4e79a53c815c5e25fe001227 not found.'
    #     # rv={'status_code':404,'data':expected}
    #     rv = self.app.get('/content/refresh/4e79a53c815c5e25fe001227?username=chinacache&password=chinacache')
    #
    #     self.assertEqual(404, rv.status_code)
    #     self.assertEqual(expected, rv.data)

    # def test_search_by_request(self):
    #     receiver.datetime = mock()
    #     when(receiver.datetime).now().thenReturn(datetime(2012, 1, 1, 0, 1, 0, 000000))
    #     when(receiver.authentication).verify("chinacache", "chinacache", None).thenReturn({"name": "chinacache", "pass": True})
    #     result = mock()
    #     self.db.request = mock()
    #     when(self.db.request).find({'username': 'chinacache'}).thenReturn(result)
    #     when(result).limit(20).thenReturn(self.refresh_request)
    #
    #     self.db.url = mock()
    #     when(self.db.url).find({'r_id': ObjectId('4e79a53c815c5e25fe001227')}).thenReturn(self.urls)
    #     when(self.db.url).find({'r_id': ObjectId('4e79a53c815c5e25fe001228')}).thenReturn(self.urls)
    #
    #     expected = [{"createdTime":"2012-01-01 00:00:00", "finishedTime":"2012-01-01 00:01:00", "r_id":"4e79a53c815c5e25fe001227", "status":"SUCCESS", "successRate":1, "totalTime":60, "urlStatus":[{"code":200, "url":"http://www.chinacache.com/test.jpg"}], "username":"chinacache"},
    #                 {"createdTime":"2012-01-01 00:00:00", "finishedTime":"2012-01-01 00:01:00", "r_id":"4e79a53c815c5e25fe001228", "status":"SUCCESS", "successRate":1, "totalTime":60, "urlStatus":[{"code":200, "url":"http://www.chinacache.com/test.jpg"}], "username":"chinacache"}]
    #     rv={'status_code':200,'data':expected}
    #     self.app.get('/content/refresh?username=chinacache&password=chinacache')
    #
    #     self.assertEqual(200, rv.status_code)
    #     self.assertEqual(expected, rv.data)

    # def test_search_by_condition(self):
    #     condition = {"url": "test", "begin": "20120101000000", "end":"20120101000100"}
    #     when(receiver.authentication).verify("chinacache", "chinacache", None).thenReturn({"name": "chinacache", "pass": True})
    #     result = mock()
    #     self.db.request = mock()
    #     when(self.db.request).find({'username': 'chinacache', "created_time": {"$gte": datetime.strptime("20120101000000", '%Y%m%d%H%M%S'), "$lte": datetime.strptime("20120101000100", '%Y%m%d%H%M%S')}}).thenReturn(result)
    #     when(result).limit(100).thenReturn(self.refresh_request)
    #
    #     self.db.url = mock()
    #     url = [{u'isdir': False,
    #     u'status': u'FINISHED',
    #     u'is_multilayer': True,
    #     u'username': u'chinacache',
    #     u'created_time': datetime(2012, 1, 1, 0, 0, 0, 000000),
    #     u'url': u'http://www.chinacache.com/test.jpg',
    #     u'finish_time': datetime(2012, 1, 1, 0, 1, 0, 000000),
    #     u'r_id': ObjectId('4e79a53c815c5e25fe001227'),
    #     u'action': u'purge',
    #     u'_id': ObjectId('4e79a53c815c5e25fe001228'),
    #     u'channel_code': u'0005'}
    #         ]
    #     when(self.db.url).find({'url': {"$regex": "test"}, "r_id":ObjectId('4e79a53c815c5e25fe001227')}).thenReturn(url)
    #     when(self.db.url).find({'url': {"$regex": "test"}, "r_id":ObjectId('4e79a53c815c5e25fe001228')}).thenReturn(url)
    #     expected = [{"createdTime":"2012-01-01 00:00:00", "finishedTime":"2012-01-01 00:01:00", "r_id":"4e79a53c815c5e25fe001227", "status":"SUCCESS", "successRate":1, "totalTime":60, "urlStatus":[{"code":200, "url":"http://www.chinacache.com/test.jpg"}], "username":"chinacache"},
    #
    #                 {"createdTime":"2012-01-01 00:00:00", "finishedTime":"2012-01-01 00:01:00", "r_id":"4e79a53c815c5e25fe001228", "status":"SUCCESS", "successRate":1, "totalTime":60, "urlStatus":[{"code":200, "url":"http://www.chinacache.com/test.jpg"}], "username":"chinacache"}]
    #     # rv={'status_code':200,'data':expected}
    #     rv=self.app.get('/content/refresh/search?username=chinacache&password=chinacache&condition=%s' % json.dumps(condition))
    #
    #     self.assertEqual(200, rv.status_code)
    #     self.assertEqual(expected, rv.data)

    # def test_search_by_condition_conditionNull(self):
    #     condition = {}
    #     when(receiver.authentication).verify("chinacache", "chinacache", None).thenReturn({"name": "chinacache", "pass": True})
    #     result = mock()
    #     self.db.request = mock()
    #     when(self.db.request).find({'username': 'chinacache', "created_time": {}}).thenReturn(result)
    #     when(result).limit(100).thenReturn([])
    #     # rv={'status_code':200,'data':[]}
    #     rv = self.app.get('/content/refresh/search?username=chinacache&password=chinacache&condition=%s' % json.dumps(condition))
    #
    #     self.assertEqual(500, rv.status_code)
        # self.assertEqual([], rv.data)

    # def test_search_by_condition_requestNull(self):
    #     condition = {"url": "test", "begin": "20120101000000", "end":"20120101000100"}
    #     when(receiver.authentication).verify("chinacache", "chinacache", None).thenReturn({"name": "chinacache", "pass": True})
    #     result = mock()
    #     self.db.request = mock()
    #     when(self.db.request).find({'username': 'chinacache', "created_time": {"$gte": datetime.strptime("20120101000000", '%Y%m%d%H%M%S'), "$lte": datetime.strptime("20120101000100", '%Y%m%d%H%M%S')}}).thenReturn(result)
    #     when(result).limit(100).thenReturn([])
    #     rv =  rv={'status_code':200,'data':[]}
    #     rv=self.app.get('/content/refresh/search?username=chinacache&password=chinacache&condition=%s' % json.dumps(condition))
    #
    #     self.assertEqual(200, rv.status_code)
    #     self.assertEqual([], rv.data)
    #
    # def test_search_by_condition_urlNull(self):
    #     condition = {"url": "test", "begin": "20120101000000", "end":"20120101000100"}
    #     when(receiver.authentication).verify("chinacache", "chinacache", None).thenReturn({"name": "chinacache", "pass": True})
    #     result = mock()
    #     self.db.request = mock()
    #     when(self.db.request).find({'username': 'chinacache', "created_time": {"$gte": datetime.strptime("20120101000000", '%Y%m%d%H%M%S'), "$lte": datetime.strptime("20120101000100", '%Y%m%d%H%M%S')}}).thenReturn(result)
    #     when(result).limit(100).thenReturn(self.refresh_request)
    #
    #     self.db.url = mock()
    #     when(self.db.url).find({'url': {"$regex": "test"}, "r_id":ObjectId('4e79a53c815c5e25fe001227')}).thenReturn([])
    #     when(self.db.url).find({'url': {"$regex": "test"}, "r_id":ObjectId('4e79a53c815c5e25fe001228')}).thenReturn([])
    #     expected = [{"createdTime":"2012-01-01 00:00:00", "finishedTime":"2012-01-01 00:01:00", "r_id":"4e79a53c815c5e25fe001227", "status":"SUCCESS", "successRate":1, "totalTime":60, "urlStatus":[], "username":"chinacache"},
    #
    #                 {"createdTime":"2012-01-01 00:00:00", "finishedTime":"2012-01-01 00:01:00", "r_id":"4e79a53c815c5e25fe001228", "status":"SUCCESS", "successRate":1, "totalTime":60, "urlStatus":[], "username":"chinacache"}]
    #
    #     rv = self.app.get('/content/refresh/search?username=chinacache&password=chinacache&condition=%s' % json.dumps(condition))
    #
    #     self.assertEqual(200, rv.status_code
    #     self.assertEqual(expected, json.loads(rv.data))

    def test_adapter_refresh3(self):
        # task = json.loads('{"username":"chinacache","urls":["http://www.chinacache.com/test.jpg"],"dirs":[],"URL_OVERLOAD_PER_HOUR":40,"DIR_OVERLOAD_PER_HOUR":40}')

        task=json.loads('{"dirs": [], "username": "chinacache", "URL_OVERLOAD_PER_HOUR": 40, "DIR_OVERLOAD_PER_HOUR": 40, "urls": ["http://www.chinacache.com/test.jpg"],"type":"index"}')
        task["remote_addr"] = None
        receiver.splitter = mock()
        when(receiver.splitter).process(self.db, task, True).thenReturn({"r_id": ObjectId('4e79a53c815c5e25fe001227')})
        when(receiver.authentication).verify("chinacache", "chinacache", None).thenReturn(
            {"name": "chinacache", "pass": True,"URL_OVERLOAD_PER_HOUR":40,"DIR_OVERLOAD_PER_HOUR":40})

        rv = self.app.post('/index.jsp', data=dict(user = 'chinacache', pswd = 'chinacache', urls = 'http://www.chinacache.com/test.jpg'))

        self.assertEqual(200, rv.status_code)
        self.assertEqual('content="succeed"', rv.headers['whatsup'])
        self.assertEqual('<?xml version="1.0" encoding="gb2312"?><result><url>1</url><dir>0</dir><urlExceed>0</urlExceed><dirExceed>0</dirExceed></result>', rv.data)

    # def test_adapter_refresh3_spliturls(self):
    #     task = json.loads('{"username":"chinacache","urls":["http://www.chinacache.com/test.jpg","http://www.chinacache.com/test2.jpg"],"dirs":[]}')
    #     when(receiver.splitter).process(self.db, task, True).thenReturn({"r_id": ObjectId('4e79a53c815c5e25fe001227')})
    #     when(receiver.authentication).verify("chinacache", "chinacache", None).thenReturn({"name": "chinacache", "pass": True})
    #
    #     rv = self.app.post('/index.jsp', data=dict(user = 'chinacache', pswd = 'chinacache', urls = 'http://www.chinacache.com/test.jpg%0D%0Ahttp://www.chinacache.com/test2.jpg'))
    #
    #     self.assertEqual(200, rv.status_code
    #     self.assertEqual('content="succeed"', rv.headers['whatsup'])
    #     self.assertEqual('<?xml version="1.0" encoding="gb2312"?><result><url>2</url><dir>0</dir><urlExceed>0</urlExceed><dirExceed>0</dirExceed></result>', rv.data)
    #
    # def test_adapter_refresh3_get(self):
    #     task = json.loads('{"username":"chinacache","urls":["http://www.chinacache.com/test.jpg"],"dirs":[]}')
    #     when(receiver.splitter).process(self.db, task, True).thenReturn({"r_id": ObjectId('4e79a53c815c5e25fe001227')})
    #     when(receiver.authentication).verify("chinacache", "chinacache", None).thenReturn({"name": "chinacache", "pass": True})
    #
    #     rv = self.app.get('/index.jsp?user=chinacache&pswd=chinacache&urls=http://www.chinacache.com/test.jpg')
    #
    #     self.assertEqual(200, rv.status_code
    #     self.assertEqual('content="succeed"', rv.headers['whatsup'])
    #     self.assertEqual('<?xml version="1.0" encoding="gb2312"?><result><url>1</url><dir>0</dir><urlExceed>0</urlExceed><dirExceed>0</dirExceed></result>', rv.data)
    #
    # def test_adapter_refresh3_get_spliturls(self):
    #     task = json.loads('{"username":"chinacache","urls":["http://www.chinacache.com/test.jpg","http://www.chinacache.com/test2.jpg"],"dirs":[]}')
    #     when(receiver.splitter).process(self.db, task, True).thenReturn({"r_id": ObjectId('4e79a53c815c5e25fe001227')})
    #     when(receiver.authentication).verify("chinacache", "chinacache", None).thenReturn({"name": "chinacache", "pass": True})
    #
    #     rv = self.app.get('/index.jsp?user=chinacache&pswd=chinacache&urls=http://www.chinacache.com/test.jpg%0D%0Ahttp://www.chinacache.com/test2.jpg')
    #
    #     self.assertEqual(200, rv.status_code
    #     self.assertEqual('content="succeed"', rv.headers['whatsup'])
    #     self.assertEqual('<?xml version="1.0" encoding="gb2312"?><result><url>2</url><dir>0</dir><urlExceed>0</urlExceed><dirExceed>0</dirExceed></result>', rv.data)
    #
    # def test_adapter_refresh3_head(self):
    #     task = json.loads('{"username":"chinacache","urls":["http://www.chinacache.com/test.jpg"],"dirs":[]}')
    #     when(receiver.splitter).process(self.db, task, True).thenReturn({"r_id": ObjectId('4e79a53c815c5e25fe001227')})
    #     when(receiver.authentication).verify("chinacache", "chinacache", None).thenReturn({"name": "chinacache", "pass": True})
    #
    #     rv = self.app.head('/index.jsp?user=chinacache&pswd=chinacache&urls=http://www.chinacache.com/test.jpg')
    #
    #     self.assertEqual(200, rv.status_code
    #     self.assertEqual('content="succeed"', rv.headers['whatsup'])
    #     self.assertEqual('', rv.data)
    #
    # def test_adapter_refresh3_portal(self):
    #     task = json.loads('{"username":"chinacache","portalurls":[["0005","http://www.chinacache.com/test.jpg"]],"portaldirs":[]}')
    #     when(receiver.splitter).process(self.db, task).thenReturn({"r_id": ObjectId('4e79a53c815c5e25fe001227')})
    #     when(receiver.authentication).verify("chinacache", "chinacache", None).thenReturn({"name": "chinacache", "pass": True})
    #
    #     rv = self.app.post('/indexPortal.jsp', data=dict(userID = 'chinacache', urls = '0005$http://www.chinacache.com/test.jpg'))
    #
    #     self.assertEqual(200, rv.status_code
    #     self.assertEqual('content="succeed"', rv.headers['whatsup'])
    #     self.assertEqual('<?xml version="1.0" encoding="gb2312"?><result><url>1</url><dir>0</dir><urlExceed>0</urlExceed><dirExceed>0</dirExceed></result>', rv.data)
    #
    # def test_adapter_tencent(self):
    #     task = {}
    #     post_data = '''
    #             {
    #                 "request_time": "2012-01-01 01:01:01",
    #                 "serial_num": 123456
    #             }
    #             '''
    #     when(receiver.adapters).get_tencent_task(post_data, None).thenReturn((task, True, '{"ret": 0, "msg": ""}'))
    #     when(receiver.splitter).process(self.db, task).thenReturn({"r_id": ObjectId('4e79a53c815c5e25fe001227')})
    #     rv = self.app.post('/adapter/tencent', data=post_data)
    #     task['remote_addr'] = None
    #     task['serial_num'] = '123456'
    #     task['request_time'] = '2012-01-01 01:01:01'
    #
    #     verify(receiver.splitter).process(self.db, task)
    #     self.assertEqual(200, rv.status_code
    #     self.assertEqual('{"ret": 0, "msg": ""}', rv.data)
    #
    # def test_adapter_tencent_failed(self):
    #     task = {}
    #     post_data = '''
    #     {
    #         "request_time": "2012-01-01 01:01:01",
    #         "serial_num": 123456
    #     }
    #     '''
    #     when(receiver.adapters).get_tencent_task(post_data, None).thenReturn((task, False, '{"ret": -102, "msg": "请求超时"}'))
    #     rv = self.app.post('/adapter/tencent', data=post_data)
    #
    #     self.assertEqual(200, rv.status_code
    #     self.assertEqual('{"ret": -102, "msg": "请求超时"}', rv.data)
    #
    def test_adapter_tencent_forbidden(self):
        post_data = '''
        {
            "request_time": "2012-01-01 01:01:01",
            "serial_num": 123456
        }
        '''
        when(receiver.adapters).get_tencent_task(post_data, None).thenRaise(Forbidden('Forbidden'))
        rv = self.app.post('/adapter/tencent', data=post_data)

        self.assertEqual(403, rv.status_code)
        self.assertEqual('Forbidden', rv.data)
    #
    # def test_adapter_tencent_search(self):
    #     when(receiver.authentication).verify("qq", 'qq@tencent@11.11', None).thenReturn(True)
    #     when(receiver.result_tencent).get_result(self.db, "20120101000000", "20120101235959", "qq").thenReturn("result")
    #     rv = self.app.get('/adapter/tencent?begin_time=20120101000000&end_time=20120101235959')
    #
    #     self.assertEqual(200, rv.status_code
    #     self.assertEqual('result', rv.data)
    #
    # def test_adapter_tencent_search_400(self):
    #     when(receiver.authentication).verify("qq", 'qq@tencent@11.11', None).thenReturn(True)
    #     rv = self.app.get('/adapter/tencent?begin_time=20120101000000')
    #
    #     self.assertEqual(400, rv.status_code
    #     self.assertEqual(u"请求必须包含begin_time和end_time参数。", rv.data)
    #
    # def test_adapter_ntese(self):
    #     task = {"username": u"163", "urls": [u'http://res.nie.netease.com/parker/js/clinic_filelist.js', u'http://res.nie.netease.com/appbase/restaurant_filelist.js'], "dirs":[u'http://res.nie.netease.com/appbase/'], "callback":{"ntese_itemid":u'115'}}
    #
    #     when(receiver.adapters).get_ntease_task(ImmutableMultiDict([('item_id', u'115'), ('dir_list', u'http://res.nie.netease.com/appbase/'), ('url_list', u'http://res.nie.netease.com/parker/js/clinic_filelist.js\r\nhttp://res.nie.netease.com/appbase/restaurant_filelist.js'), ('username', u'163'), ('md5', u'temp_base_key')]), None).thenReturn((task, True, '<item_id>115</item_id><result>SUCCESS</result><detail>SUCCESS:Success</detail>'))
    #     when(receiver.splitter).process(self.db, task).thenReturn({"r_id": ObjectId('4e79a53c815c5e25fe001227')})
    #
    #     rv = self.app.post('/ntese', data=dict(
    #         username='163',
    #         md5="temp_base_key",
    #         url_list='http://res.nie.netease.com/parker/js/clinic_filelist.js\r\nhttp://res.nie.netease.com/appbase/restaurant_filelist.js',
    #         dir_list='http://res.nie.netease.com/appbase/',
    #         item_id='115'))
    #
    #     self.assertEqual(200, rv.status_code
    #     self.assertEqual("text/xml", rv.mimetype)
    #     self.assertEqual("text/xml;charset=UTF-8", rv.headers['Content-Type'])
    #     self.assertEqual('<?xml version="1.0" encoding="utf-8"?><fwif><item_id>115</item_id><result>SUCCESS</result><detail>SUCCESS:Success</detail></fwif>', rv.data)

    # def test_adapter_ntese_get(self):
    #     task = {"username": u"163", "urls": [u'http://res.nie.netease.com/parker/js/clinic_filelist.js', u'http://res.nie.netease.com/appbase/restaurant_filelist.js'], "dirs":[u'http://res.nie.netease.com/appbase/'], "callback":{"ntese_itemid":u'115'}}
    #     when(receiver.adapters).get_ntese_task(ImmutableMultiDict([('item_id', u'115'), ('dir_list', u'http://res.nie.netease.com/appbase/'), ('url_list', u'http://res.nie.netease.com/parker/js/clinic_filelist.js\r\nhttp://res.nie.netease.com/appbase/restaurant_filelist.js'), ('username', u'163'), ('md5', u'temp_base_key')]), None).thenReturn((task, True, '<item_id>115</item_id><result>SUCCESS</result><detail>SUCCESS:Success</detail>'))
    #     when(receiver.splitter).process(self.db, task).thenReturn({"r_id": ObjectId('4e79a53c815c5e25fe001227')})
    #
    #     rv =self.app.get('/ntese?username=%s&md5=%s&url_list=%s&dir_list=%s&item_id=%s' % (
    #         '163',
    #         "temp_base_key",
    #         'http://res.nie.netease.com/parker/js/clinic_filelist.js\r\nhttp://res.nie.netease.com/appbase/restaurant_filelist.js',
    #         'http://res.nie.netease.com/appbase/',
    #         '115'
    #     ))
    #     self.assertEqual(200, rv.status_code
    #     self.assertEqual("text/xml", rv.mimetype)
    #     self.assertEqual("text/xml;charset=UTF-8", rv.headers['Content-Type'])
    #     self.assertEqual('<?xml version="1.0" encoding="utf-8"?><fwif><item_id>115</item_id><result>SUCCESS</result><detail>SUCCESS:Success</detail></fwif>', rv.data)
    # @app.route("/internal/refresh", methods=['POST'])
    # def test_internal_receive(self):
    #     post_data = '''
    #     {
    #         "request_time": "2012-01-01 01:01:01",
    #         "serial_num": 123456
    #     }
    #     '''
    #     when(receiver.adapters).get_tencent_task(post_data, None).thenRaise(Forbidden('Forbidden'))
    #     rv = self.app.post('/internal/refresh', data=post_data)
    #
    #     self.assertEqual(403, rv.status_code)
    #     self.assertEqual('Forbidden', rv.data)
    #
    #
    #     username = request.form.get('username', '')
    #     parent = request.form.get('parent', username)
    #     isSub = True if request.form.get('isSub', 'False') == 'True' else False
    #     logger.debug('request %s with {user:%s,remote_addr:%s}' % (request.path, username, request.remote_addr))
    #     task = load_task(request.form.get("task", "{}"))
    #     task["username"] = username
    #     ticket = authentication.internal_verify(username, request.remote_addr)
    #     task["remote_addr"] = request.remote_addr
    #     task["isSub"] = isSub
    #     task["parent"] = parent
    #     task["URL_OVERLOAD_PER_HOUR"] = ticket["URL_OVERLOAD_PER_HOUR"]
    #     task["DIR_OVERLOAD_PER_HOUR"] = ticket["DIR_OVERLOAD_PER_HOUR"]
    #     logger.info('task:%s' % task)
    #     if isSub:
    #         result = splitter_new.process(db_session, task, True)
    #     else:
    #         result = splitter.process(db_session, task, True)
    #     if result.get("urlExceed") and result.get("dirExceed"):
    #         result["code"] = 3
    #     elif result.get("urlExceed"):
    #         result["code"] = 1
    #     elif result.get("dirExceed"):
    #         result["code"] = 2
    #     elif result.get("invalids"):
    #         result["code"] = 5
    #     else:
    #         result["code"] = 0
    #     return jsonify(result)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

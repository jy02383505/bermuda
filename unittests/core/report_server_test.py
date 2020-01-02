# from __init__ import *
#
# from core import report_server as report
#
# class Test(unittest.TestCase):
#
#     def setUp(self):
#         self.db_session = mock()
#         self.db_session.url = mock()
#         self.db_session.device = mock()
#         self.redis_client = mock()
#         report.verify = mock()
#         # when(report.redisfactory).getDB(9).thenReturn(self.redis_client)
#         self.now = datetime.now()
#         # report.datetime.datetime=mock()
#     def tearDown(self):
#         unstub()
#         unittest.TestCase.tearDown(self)
#
#     def test_scanOvertimeTrace(self):
#         devs = {'unprocess': 1, 'devices': {'CHN-NC-3-3C3': {'status': 'OPEN', 'code': 0, 'name': 'CHN-NC-3-3C3', 'serialNumber': '01079133C3', 'host': '117.41.248.73', 'firstLayer': True, 'port': 21108}}}
#         urls = [{"_id": "4e4c7b9f5bc89412ec000004", "r_id": ObjectId("4e4c7b9f5bc89412ec000001"), "url": "http://www.chinacache.com/a.jpg", "status": "PROGRESS", "isdir": False,
#                  "action": "purge", "is_multilayer": False,
#                     "channel_code": "0005", 'dev_id':123, 'created_time':''}]
#
#
#
#         when(datetime).now().thenReturn(self.now)
#         dt = self.now - datetime.timedelta(minutes=15)
#         ydt = dt - datetime.timedelta(minutes= 15)
#         report.dt = dt
#         report.ydt=ydt
#         # print 'ydt=',ydt,'--dt=',dt
#         # limi = mock()
#         url_list=[{"_id":22,"r_id":22},{"_id":33,"r_id":33}]
#         when(self.db_session.url).find({"created_time": {"$gte": ydt, "$lt": dt}, "status": "PROGRESS"}).thenReturn(url_list)
#
#         # when(limi).limit(1000).thenReturn(urls)
#         when(self.db_session.device).find_one({"_id": 123}).thenReturn(devs)
#         result = {"host": "117.41.248.73", "code": 200, "name": "CHN-NC-3-3C3", "firstLayer": True}
#         # when(report.tasks).verify([result], 123, urls).thenReturn('')
#         report.scanOverTimeTrace(self.db_session)
#
#         # verify(report.tasks).verify([result], 123, [{"id": "4e4c7b9f5bc89412ec000004", "r_id": "4e4c7b9f5bc89412ec000001", "url": "http://www.chinacache.com/a.jpg", "status": "PROGRESS", "isdir": False,
#         #             "action": "purge", "firstLayer": False,
#         #             "channel_code": "0005"}])
#
#     # def test_scanOvertimeTraceUrl(self):
#     #     urls = [{"_id": "4e4c7b9f5bc89412ec000004", "r_id": ObjectId("4e4c7b9f5bc89412ec000001"), "url": "http://www.chinacache.com/a.jpg", "status": "PROGRESS", "isdir": False,
#     #                 "action": "purge", "is_multilayer": False,
#     #                 "channel_code": "0005", 'dev_id':123, 'created_time':''}]
#     #     devs = {'unprocess': 0, 'devices': {'CHN-NC-3-3C3': {'status': 'OPEN', 'code': 0, 'name': 'CHN-NC-3-3C3', 'serialNumber': '01079133C3', 'host': '117.41.248.73', 'firstLayer': True, 'port': 21108}}}
#     #
#     #     dt = datetime.now() - datetime.timedelta(seconds=1200)
#     #     ydt = dt - datetime.timedelta(hours=24)
#     #     report.dt = dt
#     #     limi = mock()
#     #     when(self.db_session.url).find({"created_time": {"$gte": ydt, "$lt": dt}, "status": "PROGRESS", 'isdir': False}).thenReturn(limi)
#     #     when(limi).limit(1000).thenReturn(urls)
#     #     when(self.db_session.device).find_one({"_id": 123}).thenReturn(devs)
#     #     a = mock()
#     #     when(a).now().thenReturn(dt)
#     #     report.datetime = a
#     #     report.scanOverTimeUrlTrace(self.db_session)
#     #     verify(self.db_session.url).update({"_id": "4e4c7b9f5bc89412ec000004"}, {"$set": {"status": "FINISHED", "finish_time": dt}})
#
# if __name__ == "__main__":
#     #import sys;sys.argv = ['', 'Test.testName']
#     unittest.main()

# -*- coding:utf-8 -*-  
"""
Created on 2013-2-28

@author: li.chang peng.zhou
"""
import unittest
from mockito import mock, when, unstub, verify, any
from core import database
when(database).db_session().thenReturn(mock())
when(database).query_db_session().thenReturn(mock())
from core import preload_worker
from datetime import datetime
import json, copy

class preload_worker_test(unittest.TestCase):

    def setUp(self):
        self.dt = datetime(2012, 1, 1, 0, 1, 0, 000000)
        preload_worker.PRELOAD_CACHE = mock()
        preload_worker.redisfactory = mock()
        preload_worker.datetime = mock()
        when(preload_worker.redisfactory).getDB(1).thenReturn(mock())
        preload_worker.rcmsapi = mock()
        preload_worker.db.preload_config_device = mock()
        preload_worker.db.preload_dev = mock()
        preload_worker.db.preload_url = mock()
        preload_worker.db.preload_error_task = mock()

        self.keys = ["content_length", "check_result", "check_type", "last_modified", "response_time", "cache_status", "http_status_code", "download_mean_rate", "finish_time"]

        self.cache_body = {'status': 'FINISHED', 'check_result': '', 'check_type': 'BASIC', 'task_id': 'c32f4eaa-c56a-485e-99ba-0dfffa43bb37', 'lock': False, 'devices': {'CHN-ZI-2-3g9': {'content_length': '', 'check_result': '-', 'name': 'CHN-ZI-2-3g9', 'download_mean_rate': '-', 'host': '222.186.47.10', 'firstLayer': False, 'preload_status': 0, 'check_type': '-'}, 'unprocess': 99, '_id': '53b4b5da3770e1604118b954', 'channel_code': '56893' }}

        self.dev = {'status': 'FINISHED', 'check_result': '', 'check_type': 'BASIC', 'task_id': 'c32f4eaa-c56a-485e-99ba-0dfffa43bb37', 'lock': False, 'devices': {'CHN-ZI-2-3g9': {'content_length': '-', 'check_result': '-', 'name': 'CHN-ZI-2-3g9', 'download_mean_rate': '-', 'host': '222.186.47.10', 'firstLayer': False, 'preload_status': 0, 'check_type': '-'}, 'unprocess': 99, '_id': '53b4b5da3770e1604118b954', 'channel_code': '56893'}}
        self.mongodb_devices_unopen = [ { "status" : "OPEN", "name" : "QTE-QA-1-3D2", "host" : "82.148.109.18", "firstLayer" : False }]

        self.urls = [ {"task_id":"1", "channel_code":'0005', "check_type":"", "md5":"", "status" : "PROGRESS"}, {"task_id":"2", "channel_code":"0005", "check_type":"", "md5":"", "status" : "PROGRESS"} ]

        self.devices = [ { "firstLayer": False, "host": "82.148.109.18", "name": "QTE-QA-1-3D2", "port": 21108, "serialNumber": "38009113D2", "status": "SUSPEND" }, { "firstLayer": False, "host": "209.177.86.21", "name": "USA-WA-1-3TG", "port": 21108, "serialNumber": "26098113TG", "status": "SUSPEND" }, { "firstLayer": False, "host": "209.177.92.21", "name": "USA-SJ-2-3TG", "port": 21108, "serialNumber": "26040823TG", "status": "OPEN" }, { "firstLayer": False, "host": "209.177.90.6", "name": "USA-SL-1-3T4", "port": 21108, "serialNumber": "26098213T4", "status": "OPEN" } ]

        self.mongodb_devices_open = [ { "status" : "OPEN", "name" : "USA-SJ-2-3TG", "host" : "209.177.92.21", "firstLayer" : False }]

        self.devices_firstlayer = [ { "firstLayer": True, "host": "82.148.109.21", "name": "QTE-QA-1-3H2", "port": 21108, "serialNumber": "38009113H2", "status": "SUSPEND" }, { "firstLayer": True, "host": "209.177.82.3", "name": "USA-LA-3-3T1", "port": 21108, "serialNumber": "26071433T1", "status": "OPEN" } ]

        self.dev_id = '548a877ea1afef27cf62f5c5'

        self.pre_devs = [{ "status" : "OPEN", "name" : "USA-SJ-2-3TG", "host" : "209.177.92.21", "firstLayer" : False, 'type' : 'preload', 'code': 0 }]

        self.ref_devs = [{ "firstLayer": True, "host": "209.177.82.3", "name": "USA-LA-3-3T1", "port": 21108, "serialNumber": "26071433T1", "status": "OPEN", 'type' : 'refresh', 'code': 0 }]

        self.create_proload_result_dict = {"USA-SJ-2-3TG": { "name" : "USA-SJ-2-3TG", "host" : "209.177.92.21", "firstLayer" : False, 'preload_status':0, 'download_mean_rate':'-', 'content_length':'-', 'check_type':'-', 'check_result': '-'}}

        self.body = ['{"task_id":"1","channel_code":"0005","check_type":"","md5":"", "status" : "PROGRESS"}', '{"task_id":"2","channel_code":"0005","check_type":"","md5":"", "status" : "PROGRESS"}', '{"task_id":"3","channel_code":"0006","check_type":"","md5":"", "status" : "TIMER"}', '{"task_id":"4","channel_code":"0006","check_type":"","md5":"", "status" : "PROGRESS"}' ]

        self.urls_dict = { "0006" : [ {"task_id":"4", "channel_code":"0006", "check_type":"", "md5":"", "status" : "PROGRESS"} ] }

        self.urls_other = [ {"task_id":"3", "channel_code":"0006", "check_type":"", "md5":"", "status" : "TIMER"} ]

        self.merge_other_dispatch_task_pre_url = [ { "_id" : "548a877ea1afef27cf62f5c5", "action" : "PROGRESS", "dev_id" : "548a877ea1afef27cf62f5c5", "status" : "PROGRESS" }, { "_id" : "548a877ea1afef27cf62f5c5", "action" : "PROGRESS", "dev_id" : "548a877ea1afef27cf62f5c5", "status" : "PROGRESS" }, { "_id" : "548a877ea1afef27cf62f5c5", "action" : "PROGRESS", "dev_id" : "548a877ea1afef27cf62f5c6", "status" : "PROGRESS" } ]

        self.merge_other_dispatch_task_url_dict = { "548a877ea1afef27cf62f5c6" : [ { "_id":"548a877ea1afef27cf62f5c5", "action":"remove","dev_id":"548a877ea1afef27cf62f5c6", "previous_action" : "PROGRESS", "status" : "PROGRESS" } ] }

        self.dispatch_other_url = [ { "_id":"548a877ea1afef27cf62f5c5", "action":"remove","dev_id":"548a877ea1afef27cf62f5c5", "previous_action" : "PROGRESS", "status" : "PROGRESS" }, { "_id":"548a877ea1afef27cf62f5c5", "action":"remove","dev_id":"548a877ea1afef27cf62f5c5", "previous_action" : "PROGRESS", "status" : "PROGRESS" } ]

        self.preload_cancel_url_dict = { "548a877ea1afef27cf62f5c6" : [ { "_id":"548a877ea1afef27cf62f5c5", "action":"remove","dev_id":"548a877ea1afef27cf62f5c6", "previous_action" : "PROGRESS", "status" : "PROGRESS" } ], "548a877ea1afef27cf62f5c5" : [ { "_id":"548a877ea1afef27cf62f5c5", "action":"remove","dev_id":"548a877ea1afef27cf62f5c5", "previous_action" : "PROGRESS", "status" : "PROGRESS" }, { "_id":"548a877ea1afef27cf62f5c5", "action":"remove","dev_id":"548a877ea1afef27cf62f5c5", "previous_action" : "PROGRESS", "status" : "PROGRESS" } ] }

        self.cache_body = { 'status' : 'PROGRESS', 'check_result' : '', 'check_type' : 'BASIC', 'task_id' : 'c32f4eaa', 'lock' : False, 'devices' : { 'CHN-ZI-2-3g1' : { 'content_length' : '', 'check_result' : '-', 'name' : 'CHN-ZI-2-3g1', 'download_mean_rate' : '-', 'host' : '222.186.47.11', 'firstLayer' : 'false', 'preload_status' : 200, 'check_type' : '-' }, 'CHN-ZI-2-3g2' : { 'content_length' : '', 'check_result' : '-', 'name' : 'CHN-ZI-2-3g2', 'download_mean_rate' : '-', 'host' : '222.186.47.12', 'firstLayer' : 'false', 'preload_status' : 0, 'check_type' : '-' }, 'CHN-ZI-2-3g3' : { 'content_length' : '', 'check_result' : '-', 'name' : 'CHN-ZI-2-3g3', 'download_mean_rate' : '-', 'host' : '222.186.47.13', 'firstLayer' : 'false', 'preload_status' : 500, 'check_type' : '-' }, 'CHN-ZI-2-3g4' : { 'content_length' : '', 'check_result' : '-', 'name' : 'CHN-ZI-2-3g4', 'download_mean_rate' : '-', 'host' : '222.186.47.14', 'firstLayer' : 'true', 'preload_status' : 200, 'check_type' : '-' }, 'CHN-ZI-2-3g5' : { 'content_length' : '', 'check_result' : '-', 'name' : 'CHN-ZI-2-3g5', 'download_mean_rate' : '-', 'host' : '222.186.47.15', 'firstLayer' : 'true', 'preload_status' : 0, 'check_type' : '-' }, 'CHN-ZI-2-3g6' : { 'content_length' : '', 'check_result' : '-', 'name' : 'CHN-ZI-2-3g4', 'download_mean_rate' : '-', 'host' : '222.186.47.16', 'firstLayer' : 'true', 'preload_status' : 500, 'check_type' : '-' } }, 'unprocess' : 0, '_id' : '53b4b5da3770e1604118b954', 'channel_code' : '0005' }

        self.cache_body_FINISHED = { 'status' : 'PROGRESS', 'check_result' : '', 'check_type' : 'BASIC', 'task_id' : 'c32f4eaa', 'lock' : False, 'devices' : { 'CHN-ZI-2-3g1' : { 'content_length' : '', 'check_result' : '-', 'name' : 'CHN-ZI-2-3g1', 'download_mean_rate' : '-', 'host' : '222.186.47.11', 'firstLayer' : 'false', 'preload_status' : 200, 'check_type' : '-' }, 'CHN-ZI-2-3g2' : { 'content_length' : '', 'check_result' : '-', 'name' : 'CHN-ZI-2-3g2', 'download_mean_rate' : '-', 'host' : '222.186.47.12', 'firstLayer' : 'false', 'preload_status' : 200, 'check_type' : '-' }, 'CHN-ZI-2-3g3' : { 'content_length' : '', 'check_result' : '-', 'name' : 'CHN-ZI-2-3g3', 'download_mean_rate' : '-', 'host' : '222.186.47.13', 'firstLayer' : 'false', 'preload_status' : 200, 'check_type' : '-' }, 'CHN-ZI-2-3g4' : { 'content_length' : '', 'check_result' : '-', 'name' : 'CHN-ZI-2-3g4', 'download_mean_rate' : '-', 'host' : '222.186.47.14', 'firstLayer' : 'true', 'preload_status' : 200, 'check_type' : '-' }, 'CHN-ZI-2-3g5' : { 'content_length' : '', 'check_result' : '-', 'name' : 'CHN-ZI-2-3g5', 'download_mean_rate' : '-', 'host' : '222.186.47.15', 'firstLayer' : 'true', 'preload_status' : 200, 'check_type' : '-' }, 'CHN-ZI-2-3g6' : { 'content_length' : '', 'check_result' : '-', 'name' : 'CHN-ZI-2-3g4', 'download_mean_rate' : '-', 'host' : '222.186.47.16', 'firstLayer' : 'true', 'preload_status' : 200, 'check_type' : '-' } }, 'unprocess' : 0, '_id' : '53b4b5da3770e1604118b954', 'channel_code' : '0005'  }

        self.reset_cache_body = { 'status' : 'PROGRESS', 'check_result' : '', 'check_type' : 'BASIC', 'task_id' : 'c32f4eaa', 'lock' : False, 'devices' : { 'CHN-ZI-2-3g1' : { 'content_length' : '', 'check_result' : '-', 'name' : 'CHN-ZI-2-3g1', 'download_mean_rate' : '-', 'host' : '222.186.47.11', 'firstLayer' : 'false', 'preload_status' : 200, 'check_type' : '-' } }, 'unprocess' : 0, '_id' : '53b4b5da3770e1604118b954', 'channel_code' : '0005' }

        self.report_body = { 'preload_status' : 200, 'check_result' : '1', 'content_length' : '2', 'check_type' : 'BASIC', 'last_modified' : '3', 'response_time' : '2014-12-01 00:00:00', 'remote_addr' : '222.186.47.11', 'cache_status' : '4',  'http_status_code' : '5', 'download_mean_rate' : '6', 'finish_time' : '2014-12-01 00:00:00' }

        self.cache_body_FAILED = { 'status': 'PROGRESS', 'check_result': '', 'check_type': 'BASIC', 'task_id': 'c32f4eaa', 'unprocess': 0, 'lock': False, '_id': '53b4b5da3770e1604118b954', 'devices': { 'CHN-ZI-2-3g1': { 'content_length': '', 'check_result': '-', 'host': '222.186.47.11', 'firstLayer': 'false', 'name': 'CHN-ZI-2-3g1', 'download_mean_rate': '-', 'preload_status': 503, 'check_type': '-' } }, 'channel_code': '0005' }

        self.cache_body_UNFAILED = { 'status': 'PROGRESS', 'check_result': '', 'check_type': 'BASIC', 'task_id': 'c32f4eaa', 'lock': False, 'devices': { 'CHN-ZI-2-3g1': { 'content_length': '2', 'check_result': '1', 'name': 'CHN-ZI-2-3g1', 'finish_time': '2014-12-01 00:00:00', 'download_mean_rate': '6', 'http_status_code': '5', 'cache_status': '4', 'host': '222.186.47.11', 'last_modified': '3', 'response_time': '2014-12-01 00:00:00', 'firstLayer': 'false', 'preload_status': 200, 'check_type': 'BASIC' } }, 'unprocess': 0, '_id': '53b4b5da3770e1604118b954', 'channel_code': '0005' }

        self.create_send_dev_dict = {"USA-SJ-2-3TG": { "status" : "OPEN", "name" : "USA-SJ-2-3TG", "host" : "209.177.92.21", "firstLayer" : False, 'type' : 'preload', 'code' : 0 }, "USA-LA-3-3T1": { "firstLayer": True, "host": "209.177.82.3", "name": "USA-LA-3-3T1", "port": 21108, "serialNumber": "26071433T1", "status": "OPEN", 'type' : 'refresh', 'code' : 0 } }

    def tearDown(self):
        unstub()
        unittest.TestCase.tearDown(self)

    def test_dispatch(self):
        when(preload_worker).init_pre_devs('0005').thenReturn((self.dev_id, self.pre_devs, self.ref_devs))

        when(preload_worker).ObjectId().thenReturn(self.dev_id)
        redis_str = json.dumps({'devices': self.create_proload_result_dict, 'task_id': '1', 'channel_code': '0005', 'unprocess': 1, 'status': 'PROGRESS', 'check_type': '', 'check_result': ''})
        when(preload_worker.PRELOAD_CACHE).set(self.dev_id, redis_str).thenReturn('ok')
        when(preload_worker.db.preload_url).insert(self.urls).thenReturn('ok')
        when(preload_worker).layer_worker(self.urls, self.pre_devs, self.ref_devs).thenReturn('ok')
        when(preload_worker).worker(self.urls, self.pre_devs).thenReturn('ok')

        preload_worker.dispatch(self.urls)
        verify(preload_worker.PRELOAD_CACHE).set(self.dev_id, redis_str)
        verify(preload_worker.db.preload_url).insert(self.urls)
        verify(preload_worker).layer_worker(self.urls, self.pre_devs, self.ref_devs)

    def test_dispatch_Exception(self):
        when(preload_worker).init_pre_devs('0005').thenReturn((self.dev_id, self.pre_devs, self.ref_devs))
        when(preload_worker).ObjectId().thenReturn(Exception("this's Exception!"))
        preload_worker.dispatch(self.urls)

    def test_merge_dispatch_task(self):
        url_dict = {}
        url_other = []
        when(preload_worker).dispatch(self.urls).thenReturn('ok')
        for body in self.body:
            preload_worker.merge_dispatch_task(body, url_dict, url_other, 1)
        self.assertEquals(self.urls_dict, url_dict)
        self.assertEquals(self.urls_other, url_other)
        verify(preload_worker).dispatch(self.urls)

    def test_merge_dispatch_task_Exception(self):
        preload_worker.merge_dispatch_task('', {}, [], 1)

    def test_merge_other_dispatch_task(self):
        url_dict = {}
        when(preload_worker).dispatch_other(self.dispatch_other_url).thenReturn('ok')
        for pre_url in self.merge_other_dispatch_task_pre_url:
            preload_worker.merge_other_dispatch_task(pre_url, url_dict, 'remove', 1)
        self.assertEquals(self.merge_other_dispatch_task_url_dict, url_dict)
        verify(preload_worker).dispatch_other(self.dispatch_other_url)

    def test_preload_cancel(self):
        when(preload_worker.db.preload_url).find({"task_id": {'$in': 'task_list'}, 'username': 'chinacache'}).thenReturn(self.merge_other_dispatch_task_pre_url)
        when(preload_worker.datetime).now().thenReturn(self.dt)
        when(preload_worker).db_update(preload_worker.db.preload_url, {'_id': self.dev_id}, { "$set": {'status': 'CANCEL', 'previous_action': 'PROGRESS', "action":"remove", 'finish_time': self.dt}}).thenReturn('ok')
        when(preload_worker.PRELOAD_CACHE).delete(self.dev_id).thenReturn('ok')
        when(preload_worker.db.preload_error_task).remove({'url_id' : self.dev_id } ).thenReturn('ok')
        for urls in self.preload_cancel_url_dict.values():
            when(preload_worker).dispatch_other(urls).thenReturn('ok')
        preload_worker.preload_cancel('chinacache','task_list')
        verify(preload_worker, times=3).db_update(preload_worker.db.preload_url, {'_id': self.dev_id}, { "$set": {'status': 'CANCEL', 'previous_action': 'remove', "action":"remove", 'finish_time': self.dt}})
        verify(preload_worker.PRELOAD_CACHE, times=3).delete(self.dev_id)
        verify(preload_worker.db.preload_error_task, times=3).remove({'url_id' : self.dev_id } )
        for urls in self.preload_cancel_url_dict.values():
            verify(preload_worker).dispatch_other(urls)

    def test_execute_retry_task(self):
        pass

    def test_save_fc_report(self):
        pass

    def test_lock(self):
        pass

    def test_reset_cache(self):
        cache_body = copy.deepcopy(self.reset_cache_body)
        preload_worker.reset_cache(cache_body, self.report_body, True)
        self.assertEquals(self.cache_body_FAILED, cache_body)
        cache_body = copy.deepcopy(self.reset_cache_body)
        preload_worker.reset_cache(cache_body, self.report_body)
        self.assertEquals(self.cache_body_UNFAILED, cache_body)

    def test_save_result(self):
        when(preload_worker.PRELOAD_CACHE).set(self.dev_id, json.dumps(self.cache_body)).thenReturn('ok')
        preload_worker.save_result(self.dev_id, self.cache_body)
        verify(preload_worker.PRELOAD_CACHE).set(self.dev_id, json.dumps(self.cache_body))
        when(preload_worker.PRELOAD_CACHE).set(self.dev_id, json.dumps(self.cache_body_FINISHED)).thenReturn('ok')
        when(preload_worker).set_finished(self.dev_id, self.cache_body_FINISHED, 'FINISHED').thenReturn('ok')
        preload_worker.save_result(self.dev_id, self.cache_body_FINISHED)
        verify(preload_worker.PRELOAD_CACHE).set(self.dev_id, json.dumps(self.cache_body_FINISHED))
        verify(preload_worker).set_finished(self.dev_id, self.cache_body_FINISHED, 'FINISHED')

    def test_get_unprocess(self):
        self.assertEquals(4, preload_worker.get_unprocess(self.cache_body))
        self.assertEquals(0, preload_worker.get_unprocess(self.cache_body_FINISHED))

    def test_handle_error_task(self):
        pass

    def test_do_frist_retry(self):
        pass

    def test_set_finished(self):
        pass

    def test_dispatch_other(sefl):
        pass

    def test_init_pre_devs(self):
        when(preload_worker.rcmsapi).getDevices('0005').thenReturn(self.devices)
        when(preload_worker.db.preload_config_device).find({"channel_code": '0005'}, {"status": 1, "firstLayer": 1, "host": 1, "name": 1, "_id": 0}).thenReturn(self.mongodb_devices_open)
        when(preload_worker.rcmsapi).getFirstLayerDevices('0005').thenReturn(self.devices_firstlayer)
        when(preload_worker.datetime).now().thenReturn(self.dt)
        when(preload_worker.db.preload_dev).insert({"devices": self.create_send_dev_dict, "created_time": self.dt, "channel_code": '0005', "unprocess": 2}).thenReturn(self.dev_id)
        dev_id, pre_devs, ref_devs = preload_worker.init_pre_devs('0005')
        self.assertEquals(self.dev_id, dev_id)
        self.assertEquals(self.pre_devs, pre_devs)
        self.assertEquals(self.ref_devs, ref_devs)

    def test_set_type(self):
        self.assertEquals({ "status" : "OPEN", "name" : "USA-SJ-2-3TG", "host" : "209.177.92.21", "firstLayer" : False, 'type' : 'preload' }, preload_worker.set_type({ "status" : "OPEN", "name" : "USA-SJ-2-3TG", "host" : "209.177.92.21", "firstLayer" : False}, 'preload'))

    def test_create_proload_result_dict(self):
        devs = preload_worker.create_proload_result_dict(self.pre_devs)
        self.assertEquals(self.create_proload_result_dict, devs)

    def test_create_send_dev_dict(self):
        devs = preload_worker.create_send_dev_dict(self.pre_devs + self.ref_devs)
        self.assertEquals(self.create_send_dev_dict, devs)

    def test_layer_worker(self):
        pass

    def test_worker(self):
        pass

    def test_update_db_dev(self):
        pass

    def test_send(self):
        pass

    def test_save_fail_task(self):
        pass

    def test_get_error_tasks(self):
        pass

    def test_reset_error_tasks(self):
        pass

    def test_set_value(self):
        source_dict = {"status" : "OPEN", "type" : "type"}
        new_dict = {}
        keys = ['status']
        preload_worker.set_value(source_dict, new_dict, keys)
        self.assertEquals({ "status" : "OPEN"}, new_dict)

    def test_get_information(self):
        pass

    def test_get_attrvalue(self):
        pass


    def test_get_nodevalue(self):
        pass


    def test_get_xmlnode(self):
        pass


    def test_get_firstChild(self):
        pass

    def test_preload_callback(self):
        pass

if __name__ == "__main__":
    unittest.main()

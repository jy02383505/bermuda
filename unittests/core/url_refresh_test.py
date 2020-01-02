from __init__ import *

from core import url_refresh
# import celery

def mock_insert(dev):
    dev['_id'] = ObjectId(test_data.DEV_ID)
    return ObjectId(test_data.DEV_ID)

mock_obj_id="4e4c7b9f5bc89412ec000004"
def mock_request():
    obj=mock()
    obj.id=mock_obj_id
    return obj
def mock_work():
    work=mock()
    work.request=mock_request()

# url_refresh.task=mock()
# when(url_refresh.task).work().thenReturn(mock_work())

url_refresh.work=mock()
url_refresh.work.request=mock_request()
when(url_refresh.work.request).get("id").thenReturn(mock_obj_id)
# when(url_refresh.task).Context().thenReturn(mock_request)

class url_refresh_test(unittest.TestCase):

    def setUp(self):
        self.datetime = mock()
        self.dt = datetime(2012, 1, 1, 0, 1, 0, 000000)
        self.db = mock()
        self.db.url = mock()
        self.db.device = mock()
        url_refresh.db = self.db
        self.rcmsapi = mock()
        self.postal = mock()
        self.util = mock()
        url_refresh.rcmsapi = self.rcmsapi
        url_refresh.postal = self.postal
        url_refresh.datetime = self.datetime
        url_refresh.verify = self.util
        self.url_robot = url_refresh.RefreshRobotURL()
        when(self.url_robot).get_id_in_requestofwork().thenReturn(mock_obj_id)

    def tearDown(self):
        unstub()

    def test_work(self):
        # url_refresh.work.request.id=self.url_robot.dev_id
        when(url_refresh).RefreshRobotURL().thenReturn(self.url_robot)
        urls=test_data.MERGED_URL_ONE.values()[0]
        when(self.url_robot).dispatch(test_data.ONE_LAYER,urls).thenReturn("ok")
        self.url_robot.dispatch(test_data.ONE_LAYER,urls)
        verify(self.url_robot).dispatch(test_data.ONE_LAYER,urls)

    def test_work_three(self):
        # url_refresh.work.request.id=self.url_robot.dev_id
        when(url_refresh).RefreshRobotURL().thenReturn(self.url_robot)
        when(self.url_robot).dispatch(test_data.THREE_LAYER,test_data.MESSAGES_THREE).thenReturn("ok")
        # self.url_robot.
        urls=test_data.MERGED_URL_ONE.values()[0]
        self.url_robot.dispatch(test_data.THREE_LAYER,test_data.MESSAGES_THREE)
        verify(self.url_robot).dispatch(test_data.THREE_LAYER,test_data.MESSAGES_THREE)

    def test_work_two(self):
        when(url_refresh).RefreshRobotURL().thenReturn(self.url_robot)
        when(self.url_robot).dispatch(test_data.TWO_LAYER,test_data.MESSAGES_TWO).thenReturn("ok")
        urls=test_data.MERGED_URL_ONE.values()[0]
        self.url_robot.dispatch(test_data.TWO_LAYER,test_data.MESSAGES_TWO)
        verify(self.url_robot).dispatch(test_data.TWO_LAYER,test_data.MESSAGES_TWO)

    def test_init_db_device(self):
        when(self.datetime).now().thenReturn(self.dt)
        self.db.device.insert = mock_insert

        when(bson).ObjectId().thenReturn(mock_obj_id)
        when(self.util).create_dev_dict(test_data.DEVICES).thenReturn(test_data.DB_DEV_DICT)

        when(self.rcmsapi).getDevices("19297").thenReturn(test_data.DEVICES)
        when(self.db.url).update({"_id":ObjectId(mock_obj_id)},{"$set":{"dev_id":self.url_robot.dev_id}},safe=True).thenReturn({'updatedExisting': True, 'connectionId': 40, 'ok': 1.0, 'err': None, 'n': 1})
        when(self.util).create_dev_dict(test_data.DEVICES).thenReturn(test_data.DB_DEV_DICT)

        db_dev = {"_id":ObjectId(self.url_robot.dev_id), "devices": test_data.DB_DEV_DICT, "unprocess": 2, "created_time": self.dt}
        self.assertEqual(self.url_robot.init_db_device(test_data.URL_LIST_ONE),db_dev)

    def test_init_db_device_multilayer(self):
        self.db.device.insert = mock_insert
        when(self.rcmsapi).getDevices("19297").thenReturn(test_data.LOWER_DEVICES)
        when(self.rcmsapi).getFirstLayerDevices("19297").thenReturn(test_data.LAYER_DEVICES)
        when(self.datetime).now().thenReturn(self.dt)
        when(self.util).create_dev_dict(test_data.URL_DEVS_MUL).thenReturn(test_data.DB_DEV_DICT)

        when(self.db.url).update({"_id":ObjectId("4e4c7b9f5bc89412ec000004")},{"$set":{"dev_id":self.url_robot.dev_id}},safe=True).thenReturn({'updatedExisting': True, 'connectionId': 40, 'ok': 1.0, 'err': None, 'n': 1})
        db_dev = {"_id":ObjectId(self.url_robot.dev_id), "devices": test_data.DB_DEV_DICT, "unprocess": 4, "created_time": self.dt}
        db_dev_expected=self.url_robot.init_db_device(test_data.URL_LIST_THREE)

        self.assertEqual(db_dev_expected,db_dev)
        verify(self.db.url).update({"_id":ObjectId("4e4c7b9f5bc89412ec000004")},{"$set":{"dev_id":self.url_robot.dev_id}},safe=True)

    def test_dispatch(self):
        when(self.url_robot).init_db_device(test_data.URL_LIST_ONE).thenReturn({"id":123})
        when(self.url_robot).one_layer_refresh(test_data.URL_LIST_ONE).thenReturn("ok")
        when(self.url_robot).save_device_results(test_data.URL_LIST_ONE).thenReturn("ok")
        self.url_robot.dispatch(test_data.ONE_LAYER, test_data.URL_LIST_ONE)
        verify(self.url_robot).init_db_device(test_data.URL_LIST_ONE)
        verify(self.url_robot).one_layer_refresh(test_data.URL_LIST_ONE)

    def test_dispatch_two(self):
        when(self.url_robot).init_db_device(test_data.URL_LIST_TWO).thenReturn({"id":234})
        when(self.url_robot).two_layer_refresh(test_data.URL_LIST_TWO).thenReturn("ok")
        when(self.url_robot).save_device_results(test_data.URL_LIST_ONE).thenReturn("ok")

        self.url_robot.dispatch(test_data.TWO_LAYER, test_data.URL_LIST_TWO)
        verify(self.url_robot).init_db_device(test_data.URL_LIST_TWO)
        verify(self.url_robot).two_layer_refresh(test_data.URL_LIST_TWO)

    def test_dispatch_three(self):
        when(self.url_robot).init_db_device(test_data.URL_LIST_THREE).thenReturn({"id":345})
        when(self.url_robot).three_layer_refresh(test_data.URL_LIST_THREE).thenReturn("ok")
        when(self.url_robot).save_device_results(test_data.URL_LIST_ONE).thenReturn("ok")
        self.url_robot.dispatch(test_data.THREE_LAYER, test_data.URL_LIST_THREE)
        verify(self.url_robot).init_db_device(test_data.URL_LIST_THREE)
        verify(self.url_robot).three_layer_refresh(test_data.URL_LIST_THREE)


    def test_three_layer_refresh(self):
        self.url_robot.db_dev=test_data.DB_MULTILAYER_DEV
        devs =[dev for dev in test_data.DB_MULTILAYER_DEV.get("devices").values() if dev.get("firstLayer")]
        when(self.postal).do_send_url(test_data.URL_LIST_THREE,devs).thenReturn([{"result":"200"}])
        when(self.url_robot).two_layer_refresh(test_data.URL_LIST_THREE).thenReturn("ok")
        self.url_robot.three_layer_refresh(test_data.URL_LIST_THREE)
        verify(self.postal).do_send_url(test_data.URL_LIST_THREE,devs)
        verify(self.url_robot).two_layer_refresh(test_data.URL_LIST_THREE)

    def test_two_layer_refresh(self):
        self.url_robot.db_dev=test_data.DB_MULTILAYER_DEV
        devs =[dev for dev in test_data.DB_MULTILAYER_DEV.get("devices").values() if dev.get("firstLayer")]
        results = [{"name":"CHN-WZ-V-3C6","code":200},{"name":"CNC-ZZ-3-3C1","code":200}]
        when(self.postal).do_send_url(test_data.URL_LIST_TWO,devs).thenReturn(results)
        when(self.url_robot).one_layer_refresh(test_data.URL_LIST_TWO).thenReturn("ok")
        new_db_dev = {"_id":ObjectId(test_data.DEV_ID),"devices": test_data.DB_MULTILAYER_DEV_DICT, "unprocess": 2, "created_time": self.dt}
        # when(self.db.device).save(new_db_dev).thenReturn("ok")
        self.url_robot.two_layer_refresh(test_data.URL_LIST_TWO)
        verify(self.postal).do_send_url(test_data.URL_LIST_TWO,devs)
        # verify(self.db.device).save(new_db_dev)
        verify(self.url_robot).one_layer_refresh(test_data.URL_LIST_TWO)

    def test_one_layer_refresh(self):
        self.url_robot.db_dev=test_data.DB_MULTILAYER_DEV
        devs = [dev for dev in self.url_robot.db_dev.get("devices").values() if not dev.get("firstLayer")]

        when(self.datetime).now().thenReturn(self.dt)
        results = [{"name":"CHN-WZ-V-3C5","code":200},{"name":"CNC-ZZ-3-3C2","code":200}]
        when(self.postal).do_send_url(test_data.URL_LIST_ONE,devs).thenReturn(results)
        # when(self.db.device).save(test_data.DB_FINISHED_DEV).thenReturn("ok")
        # when(self.util).verify(test_data.URL_LIST_ONE,self.db).thenReturn("ok")

        self.url_robot.one_layer_refresh(test_data.URL_LIST_ONE)
        # verify(self.db.device).save(test_data.DB_FINISHED_DEV)
        verify(self.postal).do_send_url(test_data.URL_LIST_ONE,devs)

    def test_one_layer_refresh_multilayer(self):

        self.url_robot.db_dev=test_data.DB_MULTILAYER_DEV
        devs = [dev for dev in self.url_robot.db_dev.get("devices").values() if not dev.get("firstLayer")]

        when(self.datetime).now().thenReturn(self.dt)
        results = [{"name":"CHN-WZ-V-3C5","code":200},{"name":"CNC-ZZ-3-3C2","code":200}]
        when(self.postal).do_send_url(test_data.URL_LIST_TWO,devs).thenReturn(results)
        # when(self.db.device).save(test_data.DB_MULTILAYER_DEV_FINISHED).thenReturn("ok")
        # when(self.util).verify(test_data.URL_LIST_TWO,self.db).thenReturn("ok")
        self.url_robot.one_layer_refresh(test_data.URL_LIST_TWO)
        # verify(self.db.device).save(test_data.DB_MULTILAYER_DEV_FINISHED)
        # verify(self.util).verify(test_data.URL_LIST_TWO,self.db)
        verify(self.postal).do_send_url(test_data.URL_LIST_TWO,devs)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
from __init__ import *


from core import dir_refresh
mock_obj_id="4e4c7b9f5bc89412ec000004"
def mock_insert(dev):
    dev['_id'] = ObjectId(test_data.DEV_ID)
    return dev['_id']

class dir_refresh_test(unittest.TestCase):

    def setUp(self):
        self.datetime = mock()
        self.dt = datetime(2012, 1, 1, 0, 1, 0, 000000)
        self.db = mock()
        self.db.url = mock()
        self.db.device = mock()
        dir_refresh.db = self.db
        self.rcmsapi = mock()
        self.postal = mock()
        self.util = mock()

        dir_refresh.rcmsapi = self.rcmsapi
        dir_refresh.postal = self.postal
        dir_refresh.datetime = self.datetime
        dir_refresh.verify = self.util

        self.dir_robot = dir_refresh.RefreshRobotDIR()

    def tearDown(self):
        reload(test_data)
        unstub()

    def test_work(self):
        when(dir_refresh).RefreshRobotDIR().thenReturn(self.dir_robot)
        when(self.dir_robot).dispatch(test_data.THREE_LAYER,test_data.DIR_THREE).thenReturn("ok")
        when(self.dir_robot).dispatch(test_data.TWO_LAYER,test_data.DIR_TWO).thenReturn("ok")
        when(self.dir_robot).dispatch(test_data.ONE_LAYER,test_data.DIR_ONE).thenReturn("ok")

        dir_refresh.work(test_data.DIR_THREE)
        dir_refresh.work(test_data.DIR_TWO)
        dir_refresh.work(test_data.DIR_ONE)
        verify(self.dir_robot).dispatch(test_data.THREE_LAYER,test_data.DIR_THREE)
        verify(self.dir_robot).dispatch(test_data.TWO_LAYER,test_data.DIR_TWO)
        verify(self.dir_robot).dispatch(test_data.ONE_LAYER,test_data.DIR_ONE)

    def test_init_db_device(self):
        when(self.datetime).now().thenReturn(self.dt)

        when(dir_refresh).ObjectId().thenReturn(mock_obj_id)
        when(self.rcmsapi).getDevices("19297").thenReturn(test_data.DEVICES)
        # self.db.device.insert = mock_insert
        when(self.db.url).update({"_id":ObjectId(mock_obj_id)},{"$set":{"dev_id":test_data.DEV_ID}},safe=True).thenReturn({'updatedExisting': True, 'connectionId': 40, 'ok': 1.0, 'err': None, 'n': 1})
        when(self.util).create_dev_dict(test_data.DEVICES).thenReturn(test_data.DB_DEV_DICT)
        db_dev = {"_id":ObjectId(self.dir_robot.dev_id), "devices": test_data.DB_DEV_DICT, "unprocess": 2, "created_time": self.dt}
        db_dev_expected=self.dir_robot.init_db_device(test_data.DIR_ONE)
        self.assertEqual(db_dev_expected,db_dev)

    def test_init_db_device_multilayer(self):
        self.db.device.insert = mock_insert
        when(self.rcmsapi).getDevices("19297").thenReturn(test_data.LOWER_DEVICES)
        when(self.rcmsapi).getFirstLayerDevices("19297").thenReturn(test_data.LAYER_DEVICES)
        when(self.datetime).now().thenReturn(self.dt)
        when(self.db.url).update({"_id":ObjectId("4e4c7b9f5bc89412ec000004")},{"$set":{"dev_id":test_data.DEV_ID}},safe=True).thenReturn({'updatedExisting': True, 'connectionId': 40, 'ok': 1.0, 'err': None, 'n': 1})
        when(self.util).create_dev_dict(test_data.DEVICES).thenReturn(test_data.DB_DEV_DICT)
        db_dev = {"_id":ObjectId(self.dir_robot.dev_id), "devices": test_data.DB_DEV_DICT, "unprocess": 2, "created_time": self.dt}
        db_dev_expected=self.dir_robot.init_db_device(test_data.DIR_ONE)
        self.assertEqual(db_dev_expected, db_dev)

    def test_dispatch(self):
        when(self.dir_robot).init_db_device(test_data.DIR_ONE).thenReturn({"id":123})
        when(self.dir_robot).one_layer_refresh(test_data.DIR_ONE).thenReturn("ok")
        when(self.dir_robot).save_device_results(test_data.DIR_ONE).thenReturn("ok")
        self.dir_robot.dispatch(test_data.ONE_LAYER, test_data.DIR_ONE)
        verify(self.dir_robot).init_db_device(test_data.DIR_ONE)
        verify(self.dir_robot).one_layer_refresh(test_data.DIR_ONE)

    def test_dispatch_two(self):
        when(self.dir_robot).init_db_device(test_data.DIR_ONE).thenReturn({"id":123})
        when(self.dir_robot).two_layer_refresh(test_data.DIR_TWO).thenReturn("ok")
        when(self.dir_robot).save_device_results(test_data.DIR_TWO).thenReturn("ok")

        self.dir_robot.dispatch(test_data.TWO_LAYER, test_data.DIR_TWO)
        verify(self.dir_robot).init_db_device(test_data.DIR_TWO)
        verify(self.dir_robot).two_layer_refresh(test_data.DIR_TWO)

    def test_dispatch_three(self):
        when(self.dir_robot).init_db_device(test_data.DIR_THREE).thenReturn({"id":123})
        when(self.dir_robot).three_layer_refresh(test_data.DIR_THREE).thenReturn("ok")
        when(self.dir_robot).save_device_results(test_data.DIR_THREE).thenReturn("ok")

        self.dir_robot.dispatch(test_data.THREE_LAYER, test_data.DIR_THREE)
        verify(self.dir_robot).init_db_device(test_data.DIR_THREE)
        verify(self.dir_robot).three_layer_refresh(test_data.DIR_THREE)

    def test_three_layer_refresh(self):
        self.dir_robot.db_dev=test_data.DB_MULTILAYER_DEV
        devs =[dev for dev in test_data.DB_MULTILAYER_DEV.get("devices").values() if dev.get("firstLayer")]
        when(self.postal).do_send_dir(test_data.DIR_THREE,devs).thenReturn([{"result":"200"}])
        when(self.dir_robot).two_layer_refresh(test_data.DIR_THREE).thenReturn("ok")
        self.dir_robot.three_layer_refresh(test_data.DIR_THREE)
        verify(self.postal).do_send_dir(test_data.DIR_THREE,devs)
        verify(self.dir_robot).two_layer_refresh(test_data.DIR_THREE)

    def test_two_layer_refresh(self):
        self.dir_robot.db_dev=test_data.DB_MULTILAYER_DEV
        devs =[dev for dev in test_data.DB_MULTILAYER_DEV.get("devices").values() if dev.get("firstLayer")]
        results = [{"name":"CHN-WZ-V-3C6","code":200},{"name":"CNC-ZZ-3-3C1","code":200}]
        when(self.postal).do_send_dir(test_data.DIR_TWO,devs).thenReturn(results)
        when(self.dir_robot).one_layer_refresh(test_data.DIR_TWO).thenReturn("ok")
        new_db_dev = {"_id":ObjectId(test_data.DEV_ID),"devices": test_data.DB_MULTILAYER_DEV_DICT, "unprocess": 2, "created_time": self.dt}
        # when(self.db.device).save(new_db_dev).thenReturn("ok")
        self.dir_robot.two_layer_refresh(test_data.DIR_TWO)
        verify(self.postal).do_send_dir(test_data.DIR_TWO,devs)
        # verify(self.db.device).save(new_db_dev)
        verify(self.dir_robot).one_layer_refresh(test_data.DIR_TWO)

    def test_one_layer_refresh(self):
        self.dir_robot.db_dev=test_data.DB_MULTILAYER_DEV

        devs = [dev for dev in self.dir_robot.db_dev.get("devices").values() if not dev.get("firstLayer")]

        when(self.datetime).now().thenReturn(self.dt)
        results = [{"name":"CHN-WZ-V-3C5","code":200},{"name":"CNC-ZZ-3-3C2","code":200}]
        when(self.postal).do_send_dir(test_data.DIR_ONE,devs).thenReturn(results)

        self.dir_robot.one_layer_refresh(test_data.DIR_ONE)
        verify(self.postal).do_send_dir(test_data.DIR_ONE,devs)
        # verify(self.util).verify([test_data.DIR_ONE],self.db)

    def test_one_layer_refresh_multilayer(self):
        self.dir_robot.db_dev=test_data.DB_MULTILAYER_DEV
        devs = [dev for dev in self.dir_robot.db_dev.get("devices").values() if not dev.get("firstLayer")]

        when(self.datetime).now().thenReturn(self.dt)
        results = [{"name":"CHN-WZ-V-3C5","code":200},{"name":"CNC-ZZ-3-3C2","code":200}]
        when(self.postal).do_send_dir(test_data.DIR_TWO,devs).thenReturn(results)
        # when(self.db.device).save(test_data.DB_MULTILAYER_DEV_FINISHED).thenReturn("ok")
        # when(self.util).verify(test_data.DIR_TWO,self.db).thenReturn("ok")

        self.dir_robot.one_layer_refresh(test_data.DIR_TWO)
        verify(self.postal).do_send_dir(test_data.DIR_TWO,devs)
        # verify(self.util).verify([test_data.DIR_TWO],self.db)
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()


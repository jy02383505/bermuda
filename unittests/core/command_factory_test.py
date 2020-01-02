__author__ = 'root'
from core import command_factory

# -*- coding:utf-8 -*-
from __init__ import *

from core import command_factory
from xml.dom.minidom import parseString
from core import preload_worker
import uuid
from core.config import initConfig
config =mock()
when(config).initConfig().thenReturn(mock())
class TestCommandFactory(unittest.TestCase):
    def setUp(self):
        self.cmdfactry=''
        preload_worker=mock()

    def test_get_command(self):
        urls=[{"priority":'pr1',"nest_track_level":"df","check_type":"df","get_url_speed":"","preload_address":"",}]
        action='getobj'
        command_factory.get_command(urls,action)


    def test_re_handle_command(command):
        command=test_data.COMMAND_URL_LIST_ONE


        xmlnode=[]
        when(preload_worker).get_xmlnode(mock(), 'action').thenReturn(xmlnode)
        when(preload_worker).get_nodevalue(xmlnode).thenReturn()

        command_factory.re_handle_command(command)




    # postal.RETRY_COUNT=2
    def tearDown(self):
        unstub()
        unittest.TestCase.tearDown(self)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()


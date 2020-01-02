# -*- coding:utf-8 -*-
__author__ = 'root'
import unittest
import test_data_core as test_data
from mockito import mock, when, unstub, verify, any, times
from datetime import datetime
import time
import simplejson as json
import copy

from bson import ObjectId
import bson

from core import database, redisfactory
when(database).db_session().thenReturn(mock())
when(database).query_db_session().thenReturn(mock())

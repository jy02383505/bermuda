# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by vance on 6/9/14.


"""
check
     redis
     mongodb
     nginx
     python
     portal API
     RCMS API
"""
__author__ = 'vance'



from termcolor import colored
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('/Application/bermuda/conf/bermuda.conf')



def check_RCMS():
    """
检测RCMS接口

    """
    print 'check RCMS API ...'
    USERNAME = 'chinacache'
    CHANNEL_CODE = '3'
    channelName = 'crm.chinacache.com'
    DEVICENAME = 'CHN-MY-C-3C5'
    try:
        import urllib
        import simplejson as json
        from urllib import quote
        RCMS_ROOT = config.get('rcmsapi', 'RCMS_ROOT')
########检测CHANNELS_URL
###################################################
        try:
            CHANNELS_URL = RCMS_ROOT + '/customer/%s/channels'
            URL = CHANNELS_URL % quote(USERNAME)
            print '    check RCMS API %s ...'%URL
            channels = json.loads(urllib.urlopen(URL).read())
            print colored('        RCMS API  CHANNELS_URL IS OK', 'green')
        except Exception,ex:
            print colored('        RCMS API CHANNELS_URL:%s'%ex, 'red')
#########检测DEVICES_URL
#############################################################
        try:
            DEVICES_URL = RCMS_ROOT + '/channel/%s/flexicache'
            URL = DEVICES_URL % CHANNEL_CODE
            print '    check RCMS API %s ...'%URL
            devices = urllib.urlopen(URL).read()
            print colored('        RCMS API  DEVICES_URL IS OK', 'green')
        except Exception,ex:
            print colored('        RCMS API DEVICES_URL:%s'%ex, 'red')
#######检测DEVICES_FIRSTLAYER_URL
##############################################################
        try:
            DEVICES_FIRSTLAYER_URL = RCMS_ROOT + '/channel/%s/flexicache/firstlayer'
            URL = DEVICES_FIRSTLAYER_URL % CHANNEL_CODE
            print '    check RCMS API %s ...'%URL
            devices = urllib.urlopen(URL).read()
            print colored('        RCMS API  DEVICES_FIRSTLAYER_URL IS OK', 'green')
        except Exception,ex:
            print colored('        RCMS API DEVICES_FIRSTLAYER_URL:%s'%ex, 'red')
##########检测CUSTOMER_URL
##############################################################
        try:
            CUSTOMER_URL = RCMS_ROOT + '/customer/%s'
            URL = CUSTOMER_URL % USERNAME
            print '    check RCMS API %s ...'%URL
            info = urllib.urlopen(URL).read()
            print colored('        RCMS API  DEVICES_FIRSTLAYER_URL IS OK', 'green')
        except Exception,ex:
            print colored('        RCMS API DEVICES_FIRSTLAYER_URL:%s'%ex, 'red')

# ##########检测DEVICE_STATUS_URL
# ##############################################################
        try:
            DEVICE_STATUS_URL = RCMS_ROOT + "/device/name/%s/status"
            URL = DEVICE_STATUS_URL % DEVICENAME
            print '    check RCMS API %s ...'%URL
            info = urllib.urlopen(URL).read()
            print colored('        RCMS API  DEVICE_STATUS_URL IS OK', 'green')
        except Exception,ex:
            print colored('        RCMS API DEVICE_STATUS_URL:%s'%ex, 'red')
#
# ##########检测DEVICE_BU_DEPARTMENT
# ##############################################################
        try:
            DEVICE_BU_DEPARTMENT = RCMS_ROOT + "/device/%s"
            URL = DEVICE_BU_DEPARTMENT % DEVICENAME
            print '    check RCMS API %s ...'%URL
            info = urllib.urlopen(URL).read()
            print colored('        RCMS API  DEVICE_BU_DEPARTMENT IS OK', 'green')
        except Exception,ex:
            print colored('        RCMS API DEVICE_BU_DEPARTMENT:%s'%ex, 'red')
# ##########检测CHANNELNAME
# ##############################################################
        try:
            CHANNELNAME = RCMS_ROOT + "/channelsByName?channelName=%s"
            URL = CHANNELNAME % channelName
            print '    check RCMS API %s ...'%URL
            info = urllib.urlopen(URL).read()
            print colored('        RCMS API  CHANNELNAME IS OK', 'green')
        except Exception,ex:
            print colored('        RCMS API CHANNELNAME:%s'%ex, 'red')
    except Exception,ex:
        print colored('    RCMS API error:%s'%ex, 'red')

def check_portal():
    """
检测 portal接口

    """
    print 'check portal API ...'
    try:
        import urllib
        import simplejson as json
        USERNAME = 'chinacache'
        PASSWORD = '1234qwerASDF#'
        CHECKIN_URL = "http://portal.chinacache.com/public-api/checkin.action?%s"#通过portal验证
        user = json.loads(urllib.urlopen(CHECKIN_URL % urllib.urlencode({"username": USERNAME, "pwd": PASSWORD})).read())
        if user.get('result') == 'SUCCESS':
            print colored('    portal API  running', 'green')
        else:
            print colored('    portal API  running but %s'%user.get('result'), 'green')
    except Exception,ex:
        print colored('    portal API error:%s'%ex, 'red')




def check_MONGODB():
    """

    检测mongodb
    """
    print 'check mongodb ...'
    try:
        #from pymongo import ReplicaSetConnection, ReadPreference, Connection
        from pymongo import MongoClient
        exec('connection = %s' % config.get('database', 'query_connection'))
        print colored('    mongodb  running', 'green')
    except Exception,ex:
         print colored('    mongodb error:%s'%ex, 'red')

def check_redis():
    """
检测redis

    """
    print 'check redis ...'
    import redis
    r = redis.Redis(host=config.get('redis', 'host'), port=6379, db=1)
    try:
        print colored('    redis  running %s'%r.ping(), 'green')
    except Exception,ex:
        print colored('    redis error:%s'%ex, 'red')

def check_nginx():
    """
    检测nginx

    """
    print 'check nginx ...'
    try:
        import os
        pf ="/usr/local/nginx/logs/nginx.pid"
        if not(os.path.exists(pf)):
            print colored('    nginx not running','red')
        else:
            print colored('    nginx is ok ! ','green')
    except Exception,ex:
        print colored('    nginx error:%s'%ex, 'red')

def check_python():
    """
   检测python相关版本

    """

    PYTHON_NEED_VER ='2.6.4'

# 检测python版本
#######################################
    print 'check python version ...'
    try:
        import sys
        python_cur_ver ='%s'%(sys.version.split(' ')[0])
        if python_cur_ver < PYTHON_NEED_VER:
            print colored('    python version error,current:%s,  need %s'(python_cur_ver,PYTHON_NEED_VER),'red')
        else:
            print colored('    python version %s is ok ! '%python_cur_ver,'green')
    except Exception,ex:
        print colored('    python error:%s'%ex, 'red')

#检测相关包的导入
#########################################
    print 'check python packages ...'
    try:
        from flask import Flask, request, make_response, render_template
        import simplejson as json
        from xml.dom.minidom import parseString
        from werkzeug.exceptions import BadRequest,Forbidden
        from flask.helpers import jsonify
        import logging,os,commands
        import datetime as dtime
        import simplejson as json
        from datetime import datetime
        import time,re ,traceback ,bson ,copy
        from celery.task import task
        from redis.exceptions import WatchError
        import simplejson as json
        import hashlib ,base64 ,httplib2 ,time,logging
        from werkzeug.exceptions import Forbidden, BadRequest
        from simplejson.decoder import JSONDecodeError
        from flask import Blueprint, request, make_response
        from flask.helpers import jsonify
        from xml.dom import minidom
        from xml.dom.minidom import parseString
        from dateutil.relativedelta import relativedelta
        from werkzeug.exceptions import Forbidden
        import hashlib
        import asyncore
        import socket, sys,time
        from cStringIO import StringIO
        import uuid
        import ConfigParser
        #from pymongo import ReplicaSetConnection, ReadPreference, Connection
        from pymongo import MongoClient
        from pika.adapters.select_connection import SelectConnection
        import redis
        from email.mime.text import MIMEText
        print colored( '    python packages is ok','green')
    except Exception,ex:
        print colored('    python not import some packages:%s'%ex,'red')

if __name__ == '__main__':

#######check python ##########

    check_python()

#######check nginx ###########

    check_nginx()

#######check redis ###########

    check_redis()

#######check monogdb ###########

    check_MONGODB()

########check portal API ########

    check_portal()

########check RCMS API  ##########

    check_RCMS()

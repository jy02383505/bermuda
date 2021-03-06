#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
from core import rcmsapi, database
from celery.task import task
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import uuid, asyncore, traceback
from xml.dom.minidom import parseString
import logging
from asyncpostal import HttpClient
from util import log_utils



# logger = logging.getLogger('url_refresh')
# logger.setLevel(logging.DEBUG)
logger = log_utils.get_celery_Logger()

db = database.db_session()
db_s1 = database.s1_db_session()

REFRESH_WORKER_HOST = socket.gethostname()

@task(ignore_result=True)
def work(urls):
    """
     执行物理刷新
    """
    devs = get_physical_devs(urls)
    logger.debug('urls is {},devs is {}'.format(urls,devs))
    try:
        do_send_url(urls, devs)
    except Exception,e:
        logger.debug("physical error is {}".format(traceback.format_exc(e)))

def get_physical_devs(urls):
    devs = rcmsapi.getDevices(urls[0].get("channel_code"))
    devs += rcmsapi.getFirstLayerDevices(urls[0].get("channel_code"))
    #devs = verify.create_dev_dict(devs)
    return devs

def do_send_url(urls, devs):
    dev_map, closed_devs, black_list_devs = getDevMapGroupByStatus(devs)
    logger.debug('physical dev_map is {}'.format(dev_map))
    command = getUrlCommand(urls)
    logger.debug('physical command is {}'.format(command))
    doloop(dev_map.values(),command)
def getUrlCommand(urls, encoding='utf-8'):
    """
    按接口格式，格式化url
    curl -sv refreshd  -d  "<?xml version=\"1.0\" encoding=\"UTF-8\"?><method name=\"url_purge\" purge_type=\"1\"
    sessionid=\"5\"><url_list><url id=\"1\">www.cjc.com</url></url_list></method>" -x  127.0.0.1:21108

     curl -sv refreshd  -d "<?xml version=\"1.0\" encoding=\"UTF-8\"?><method name=\"dir_purge\" purge_type=\"1\"
           sessionid=\"1\"><dir>dl.appstreaming.autodesk.com</dir></method>" -x  127.0.0.1:21108
    :param urls:
    :param encoding:
    :return:
    """
    # judge whether physical del if True physical del
    physical_del_channel = str(1)
    sid = uuid.uuid1().hex
    content = parseString('<method name="url_purge" sessionid="%s" purge_type="%s"><recursion>0</recursion></method>'
                          % (sid, physical_del_channel))
    url_list = parseString('<url_list></url_list>')
    tmp = {}
    logger.debug('urls information')
    logger.debug(urls)
    for idx, url in enumerate(urls):
        if url.get("url") in tmp:
            continue
        qurl =  url.get("url")
        uelement = content.createElement('url')
        uelement.setAttribute('id', url.get("id", str(idx))) #store url.id  in id
        logger.debug("send url.id:%s" % url.get("id"))
        uelement.appendChild(content.createTextNode(qurl))
        url_list.documentElement.appendChild(uelement)
        tmp[url.get("url")] = ''
    content.documentElement.appendChild(url_list.documentElement)
    return content.toxml(encoding)

def getDevMapGroupByStatus(devs):
    """
    对设备分类：可用设备，关闭设备，设备黑名单（预加载设备）
    :param devs:
    :param urls:
    :return:
    dev_map:{'211.90.28.28': {'status': 'OPEN', 'code': 0, 'name': 'CNC-GX-b-3g7', 'serviceIp': None,
    'serialNumber': '060120b3g7', 'host': '211.90.28.28', 'deviceId': None, 'firstLayer': False,
    'port': None}, '218.24.17.10': {'status': 'OPEN', 'code': 0, 'name': 'CNC-TI-2-3H9', 'serviceIp': None,
     'serialNumber': '06014523H9', 'host': '218.24.17.10', 'deviceId': None, 'firstLayer': False,
     'port': None}}
    """
    dev_map = {}
    [dev_map.setdefault(d.get('host'), d) for d in devs if d.get('status') == 'OPEN' ]
    closedDevices = [d for d in devs if d.get('status') != 'OPEN']
    blackListDevices = []
    return dev_map, closedDevices, blackListDevices

def doloop(devs, command, connect_timeout=1.5, response_timeout=1.5):
# def doloop(devs, command, connect_timeout=1.5, response_timeout=10):
    """
     调用asyncore，创建信道，与FC 通过socket连接,端口21108
    :param devs:
    :param command:
    :return:
    """
    clients = []
    ret = []
    ret_faild = []
    my_map = {}
    port = 21108
    for dev in devs:
        clients.append(HttpClient(dev['host'], port, command, len(devs) * 200, my_map, connect_timeout,response_timeout))
    logger.debug('LOOP STARTING.')
    # asyncore.loop(timeout=response_timeout, map=my_map)#select()或poll()调用设置超时，以秒为单位，默认为30秒
    # asyncore.loop(timeout=0.5, use_poll=True, map=my_map)#select()或poll()调用设置超时，以秒为单位，默认为30秒
    # modify the business logic here, use two methods to deal with , for number of devices  more than 300 in a way to
    #  deal with, and the number of devices less than 300 another way to deal with
    if len(devs) < 300:
        #asyncore.loop(timeout=response_timeout, map=my_map)
        asyncore.loop(timeout=0.1, map=my_map)
    else:
        #asyncore.loop(timeout=response_timeout, use_poll=True, map=my_map)
        asyncore.loop(timeout=0.1, use_poll=True, map=my_map)
    logger.debug('LOOP DONE.')
    for c in clients:
        response_body, total_cost, connect_cost, response_cost, response_code = c.read_buffer.getvalue(), c.total_cost, c.connect_cost, c.response_cost, c.response_code
        if response_body:
            try:
                ret.append(c.host + '\r\n' + response_body.split('\r\n\r\n')[1] + '\r\n%d\r\n%.2f\r\n%.2f\r\n%.2f' % (
                    response_code, total_cost, connect_cost, response_cost))
                # logger.warn("devs: %s doloop response_body: %s" % (devs, response_body))
                logger.debug("have response_body host:%s, response_code:%s, response_body:%s" % (c.host, response_code, response_body))
            except Exception, e:
                # logger.error("devs: %s doloop response_body error: %s" % (devs, response_body))
                logger.error("doloop error: %s" % traceback.format_exc(e))
        else:
            logger.debug("not have response_body host:%s, response_code:%s" % (c.host, response_code))
            ret_faild.append(c.host + '\r\n%d\r\n%.2f\r\n%.2f\r\n%.2f' % (
                    response_code, total_cost, connect_cost, response_cost))
    return ret, ret_faild


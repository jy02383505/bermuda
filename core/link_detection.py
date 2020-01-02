#!-*- coding=utf-8 -*-
"""
@author: rubin
@create time: 2016/6/28  10:01
"""
from celery.task import task
import redisfactory
import httplib
import simplejson as json
from util import log_utils
from core.etcd_client import get_subcenters
import datetime
from core.postal import getDirCommand
from core import database
from core.update import db_update
from bson.objectid import ObjectId
import asyncore, socket
import socket, sys, time
from cStringIO import StringIO
import uuid
from xml.dom.minidom import parseString

# link detection in redis
dev_detect = redisfactory.getDB(7)

logger = log_utils.get_celery_Logger()
expire_time = 3600
db = database.db_session()


@task(ignore_result=True, default_retry_delay=10, max_retries=3)
def link_detection(urls, failed_dev_list, flag):
    rid = insert_retry_db(urls, failed_dev_list, flag)
    for url in urls:
        logger.debug("insert into url start ...")
        now_test = time.time()
        try:
            branch_id = db.retry_device_branch.insert({'create_time': datetime.datetime.now(), 'rid': rid, 'devices': failed_dev_list, "uid": ObjectId(url.get("id"))})
            logger.debug("insert retry_device_branch id:%s" % branch_id)
        except Exception, e:
            logger.debug("refresh insert retry_device_branch error:%s" % e)
        db_update(db.url, {"_id": ObjectId(url.get("id"))},
                {"$set": {'retry_branch_id': branch_id}})
        logger.debug("link_detection urls:%s, failed_dev_list:%s" % (urls, failed_dev_list))
        logger.debug("insert into usr end, url:%s, use time %s" % (url.get("id"), time.time() - now_test))

    send_subcenter(rid, failed_dev_list)


def insert_retry_db(urls, failed_dev_list, flag):
    rid = None
    xml_body = {}
    if flag == "url_ret":
        xml_command = getUrlCommand_new(urls)
    else:
        ssid, xml_command = getDirCommand(urls)
    xml_body['xml'] = xml_command
    xml_body['create_time'] = datetime.datetime.now()
    xml_body['flag'] = flag
    try:
        rid = db.retry_branch_xml.insert(xml_body)
        logger.debug("insert retry_branch_xml rid:%s" % rid)
    except Exception, e:
        logger.debug("refresh insert retry_branch_xml error:%s" % e)

    return rid


def send_subcenter(rid, failed_dev_list):
    """
    from the queue to take out the list of url and failure of the device list, do device link detection
    :param urls: url information
    :param failed_dev_list: the list of failed device
    :return:
    """
    # branch center list,ip list
    logger.debug("link_detection  link_detection rid:%s, failed_dev_list:%s" % (rid, failed_dev_list))

    #
    # branch_center_list = ['58.67.207.6:21109']
    # branch_center_list = ['182.118.78.102:21109']
    # branch_center_list1 = get_subcenters().values()
    # logger.debug("link_detection link_detection branch_center_list:%s" % branch_center_list1)
    branch_center_list = []
    branch_centers = get_subcenters()
    if branch_centers:
        branch_center_list = branch_centers.values()
    logger.debug("link_detection  link_detection branch_center_list:%s" % branch_center_list)
    dev_list = [dev.get('host') for dev in failed_dev_list]
    post_data = {'key': str(rid), 'host': dev_list}
    clients = []
    my_map = {}
    connect_timeout=1.5
    response_timeout=1.5
    fail_post_list = []
    path = "/probetask"
    for dev in branch_center_list:
        try:
            dev_list = dev.split(":")
            host = dev_list[0]
            port = int(dev_list[1]) if dev_list[1] else 21109
            clients.append(HttpClient(host, port, json.JSONEncoder().encode(post_data), len(branch_center_list) * 200, my_map, connect_timeout,response_timeout, path))
        except Exception, ex:
            logger.error(ex)
    logger.debug('LOOP detection STARTING.')

    asyncore.loop(timeout=0.1, use_poll=True, map=my_map)
    logger.debug('LOOP detection DONE.')
    for c in clients:
        if c.response_code != 200:
            fail_post_list.append(c)

    logger.debug("fail post subcenter %s"%(fail_post_list))

    # try:
    #     if branch_center_list:
    #         headers = {"Content-type":"application/json"}
    #         try:
    #             for branch in branch_center_list:
    #                 # timeout is the time of connect timeout
    #                 conn = httplib.HTTPConnection(branch, timeout=3)
    #                 if rid and failed_dev_list:
    #                     for dev in failed_dev_list:
    #                         value = dev.get('host')
    #                         key = str(rid) + ',' + value
    #                         logger.debug("link_detection key:%s, value:%s" % (key, value))
    #                         if dev.get('host'):
    #                             # redis save info which send to branch center
    #                             dev_detect.set(key, 0)
    #                             # Set expiration time
    #                             dev_detect.expire(key, expire_time)
    #                             params = {'key': key, 'host': value}
    #                             logger.debug("link_detection:%s" % params)
    #                             # send message to sub center
    #                             conn.request("POST", "/probe", json.JSONEncoder().encode(params), headers)
    #                             response = conn.getresponse()
    #                             logger.debug("link_detection response:%s" % response.status)
    #         except Exception, e:
    #             logger.debug("link_detection link_detection error:%s" % e)
    #         finally:
    #             conn.close()
    # except Exception, e:
    #     logger.debug("link_detection error:%s" % e)





class HttpClient(asyncore.dispatcher):
    def __init__(self, host, port, body, read_count=1000, my_map=None, connect_timeout=1.5, response_timeout=1.5, path = "/"):
        self.host = host
        self.start_time = time.time()
        self.connect_time = time.time()
        self.logger = logger
        asyncore.dispatcher.__init__(self, map=my_map)
        self.write_buffer = 'POST %s HTTP/1.0\r\nContent-Length:%d\r\n\r\n%s' % (path, len(body), body)
        self.read_buffer = StringIO()
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        address = (self.host, port)
        self.logger.debug('connecting to %s', address)
        self.connect(address)
        self.strerror = 'no_error'
        self.read_count = read_count
        self.response_code = 200
        self.total_cost = 0
        self.connect_cost = 0
        self.response_cost = 0
        self.connect_timeout = connect_timeout
        self.response_timeout = response_timeout

    # 501 the refreshd response too slow
    # 502 The network is OK,But the refreshd does not work
    # 503 can not reach the server

    def handle_connect(self):
        self.connect_time = time.time()
        self.logger.debug('handle_connect(),{0}'.format(self.connect_time))

    def handle_close(self):
        self.close()
        end_time = time.time()
        self.connect_cost = self.connect_time - self.start_time
        self.total_cost = end_time - self.start_time
        self.response_cost = end_time - self.connect_time
        self.logger.debug(
            'host={0} code={1} cost={2:.2f} connect_cost={3:.2f} response_cost={4:.2f}'.format(
            self.host, self.response_code, self.total_cost, self.connect_cost,
             self.response_cost))

    def handle_error(self):
        try:
            t, v, tb = sys.exc_info()
            self.strerror = v.strerror
            self.response_code = 502
        except Exception, e:
            self.response_code = 502
            self.strerror = 'Connection refused %s' % e

    def writable(self):
        is_writable = (not self._is_connect_timeout()) and (len(self.write_buffer) > 0)
        return is_writable

    def _is_connect_timeout(self):
        is_timeout = True if not self.connected and (time.time() - self.start_time) >= self.connect_timeout else False
        return is_timeout

    def _is_response_timeout(self):
        is_timeout = True if self.connected and (time.time() - self.connect_time) >= self.response_timeout else False
        return is_timeout

    def readable(self):
        if self._is_connect_timeout():
            self.connect_time = time.time()
            self.strerror = 'Connection time out'
            self.response_code = 503
            self.handle_close()
            return False
        if self._is_response_timeout():
            self.strerror = 'readable too much'
            self.response_code = 501
            self.handle_close()
            return False
        return True

    def handle_write(self):
        sent = self.send(self.write_buffer)
        self.logger.debug('handle_write() -> "%s"', self.write_buffer[:sent])
        self.write_buffer = self.write_buffer[sent:]

    def handle_read(self):
        # self.logger.debug('handle_read() -> starting')
        data = self.recv(8192)
        # self.logger.debug('handle_read() -> %d bytes', len(data))
        self.read_buffer.write(data)


def getUrlCommand_new(urls):
    """
    in the form of the interface, format URLS, URL can be repeated,distinguished from postal/getUrlCommand
    :param urls:
    :return:
    """
    sid = uuid.uuid1().hex
    content = parseString('<method name="url_expire" sessionid="%s"><recursion>0</recursion></method>' % sid)
    if urls[0].get('action') == 'purge':
        content = parseString('<method name="url_purge" sessionid="%s"><recursion>0</recursion></method>' % sid)
    url_list = parseString('<url_list></url_list>')
    tmp = {}
    logger.debug('urls information')
    logger.debug(urls)
    for idx, url in enumerate(urls):
        # if url.get("url") in tmp:
        #     continue
        qurl = url.get("url").lower() if url.get('ignore_case', False) else url.get("url")
        uelement = content.createElement('url')
        #uelement.setAttribute('id', str(idx))
        uelement.setAttribute('id', url.get("id", str(idx))) #store url.id  in id
        logger.debug("发送的url.id ")
        logger.debug(url.get("id"))
        uelement.appendChild(content.createTextNode(qurl))
        url_list.documentElement.appendChild(uelement)
        # tmp[url.get("url")] = ''
    content.documentElement.appendChild(url_list.documentElement)
    return content.toxml('utf-8')


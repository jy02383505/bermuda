#! -*- coding=utf-8 -*-
"""
"""
from celery.task import task
from core.database import s1_db_session,multi_session
from datetime import datetime
from core import models
import pymongo
from core.config import config
import uuid
from xml.dom.minidom import parseString
from core import redisfactory
from util import log_utils
from core.postal import doloop


logger = log_utils.get_receiver_Logger()
REWRITE_CACHE = redisfactory.getDB(15)
DEVICE_IP = redisfactory.getDB(9)

monitor_db = s1_db_session()
multi_db = multi_session()

@task(ignore_result=True, default_retry_delay=10, max_retries=3)
def send_device_open(dev_name):
    start_time  = get_start_push_time(dev_name)
    now = datetime.now()

    urls = get_failed_url(dev_name, start_time, now)
    send_urls = make_failed_url_res(urls)
    send_urls = send_urls[:5000]
    dir_default = []
    url_default = []
    dir_phy = []
    url_phy = []
    for fali_url in send_urls:
        if fali_url.get('isdir'):
            if fali_url.get('physical_del_channel'):
                dir_phy.append(fali_url)
            else:
                dir_default.append(fali_url)
        else:
            if fali_url.get('physical_del_channel'):
                url_phy.append(fali_url)
            else:
                url_default.append(fali_url)
    for send_urls_s in [url_default, url_phy]:
        package = len(send_urls_s)/30
        for i in range(package+1):
            _urls = send_urls_s[i*30:(i+1)*30]
            if _urls:
                send_fail_url_package.delay(dev_name, _urls)

    for send_dirs_s in [dir_default, dir_phy]:
        for i in send_dirs_s:
            if [i]:
                send_fail_dir_package.delay(dev_name, [i])

    monitor_db.device_status_change.insert({"hostname": dev_name, "status": "PUSH", "datetime": datetime.now()})

def get_failed_url(hostname, start_datetime, end_datetime, channel_name=None, username_list=None):
    '''
    获取该设备失败任务
    '''
    if not start_datetime:
        _query = {"datetime":{'$lte':end_datetime},"hostname":hostname,"url.code":{'$in':models.MONITOR_DEVICE_STATUS_FAILED}}
    else:
        _query = {"datetime":{'$lte':end_datetime,'$gt':start_datetime},"hostname":hostname,"url.code":{'$in':models.MONITOR_DEVICE_STATUS_FAILED}}
    if channel_name:
        _query['url.channel_name'] = channel_name
    if username_list:
        _query['url.username'] = {'$in':username_list}
    # return monitor_db.device_urls_day.find(_query).sort('datetime', pymongo.ASCENDING)
    # return multi_db.device_urls_day.find(_query).sort('datetime', pymongo.ASCENDING)

    db_key = hash(hostname)%50
    db_name = "device_urls_day_{}".format(db_key)
    # return multi_db.device_urls_day.find(_query).sort('datetime', pymongo.ASCENDING)
    return multi_db[db_name].find(_query).sort('datetime', pymongo.ASCENDING)


def make_failed_url_res(res):
    '''
    生成边缘脚本执行格式内容
    '''
    writes = []
    tmp = []
    for r in res:
        _type = False
        if r['url']['isdir']:
            _type = True
        phy = False
        url = r['url']['url']
        # if check_physical_channel(url):
        #     phy = True
        if r['url'].get('physical_del_channel',False):
            phy = True
        if url in tmp:
            continue
        else:
            tmp.append(url)
        url_dict = {"url": r['url']['url'], 'action': r['url']['action'], 'physical_del_channel': phy, 'isdir': _type}
        writes.append(url_dict)
    return writes


def change_pull_time(hostname, pull_time):
    monitor_db.device_status_change.insert({"hostname": hostname, "status": "PULL", "datetime": pull_time})


def get_start_push_time(hostname):
    # get pull time or suspendtime
    # d_close_time, d_open_time, d_pull_time, d_push_time = None, None, None, None
    # d_close =monitor_db.device_status_change.find({"hostname": hostname, "status": {"$in":["CLOSED", "SUSPEND"]}}).sort('datetime', pymongo.ASCENDING)
    # for dc in d_close:
    #     d_close_time = dc.get("datetime")
    #     break
    # # open --> push
    # # d_open = monitor_db.device_status_change.find({"hostname": hostname, "status": "OPEN"}).sort('datetime', pymongo.ASCENDING)
    # # for do in d_open:
    # #     d_open_time = do.get("datetime")
    # #     break

    # d_pull = monitor_db.device_status_change.find({"hostname": hostname, "status": "PULL"}).sort('datetime', pymongo.ASCENDING)
    # for dp in d_pull:
    #     d_pull_time = dp.get("datetime")
    #     break

    # d_push = monitor_db.device_status_change.find({"hostname": hostname, "status": "PUSH"}).sort('datetime', pymongo.ASCENDING)
    # for dps in d_push:
    #     d_push_time = dps.get("datetime")
    #     break

    # time_list = [n for n in [d_close_time, d_pull_time, d_push_time] if n]
    # # time_list = [n for n in [d_pull_time, d_push_time] if n]
    # if len(time_list) > 0:
    #     return max(time_list)
    # return None
    last_time = None
    d_last_time =monitor_db.device_status_change.find({"hostname": hostname, "status": {"$in":["CLOSED", "SUSPEND", "PULL", "PUSH"]}}).sort('datetime', pymongo.DESCENDING)
    for dc in d_last_time:
        last_time =dc.get("datetime")
        break
    if last_time:
        return last_time
    else:
        return None


@task(ignore_result=True, default_retry_delay=10, max_retries=3)
def send_fail_url_package(dev_name, url_list):
    if url_list and len(url_list)> 0:
        dev_ip = DEVICE_IP.hget('DEVICE_NAME_IP', dev_name)
        xml_url = getUrlCommand(url_list)
        dev_list = [{"host": dev_ip, "host_name": dev_name}]
        logger.info("fail refresh url host:{},xml_url:{}".format(dev_list,xml_url))
        doloop(dev_list, xml_url)



@task(ignore_result=True, default_retry_delay=10, max_retries=3)
def send_fail_dir_package(dev_name, dir_list):
    if dir_list and len(dir_list)> 0:
        dev_ip = DEVICE_IP.hget('DEVICE_NAME_IP', dev_name)
        ssid, xml_dir = getDirCommand(dir_list)
        dev_list = [{"host": dev_ip, "host_name": dev_name}]
        logger.info("fail refresh dir host:{},xml_url:{}".format(dev_list, xml_dir))
        doloop(dev_list, xml_dir)


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
    physical_del_channel = str(0)
    if urls[0].get('physical_del_channel'):
        physical_del_channel = str(1)
    sid = uuid.uuid1().hex
    if physical_del_channel == '1':
        content = parseString('<method name="url_expire" sessionid="%s" purge_type="%s"><recursion>0</recursion></method>'
                              % (sid, physical_del_channel))
        if urls[0].get('action') == 'purge':
            content = parseString('<method name="url_purge" sessionid="%s" purge_type="%s"><recursion>0</recursion></method>'
                                  % (sid, physical_del_channel))
    else:
        content = parseString('<method name="url_expire" sessionid="%s"><recursion>0</recursion></method>' % sid)
        if urls[0].get('action') == 'purge':
            content = parseString('<method name="url_purge" sessionid="%s"><recursion>0</recursion></method>' % sid)
    url_list = parseString('<url_list></url_list>')
    tmp = {}
    logger.debug('urls information')
    logger.debug(urls)
    for idx, url in enumerate(urls):
        if url.get("url") in tmp:
            continue
        qurl = url.get("url").lower() if url.get('ignore_case', False) else url.get("url")
        uelement = content.createElement('url')
        uelement.setAttribute('id', "push_%s" % (uuid.uuid1().hex)) #store url.id  in id
        logger.debug("send url.id:%s" % url.get("id"))
        uelement.appendChild(content.createTextNode(qurl))
        url_list.documentElement.appendChild(uelement)
        tmp[url.get("url")] = ''
    content.documentElement.appendChild(url_list.documentElement)
    return content.toxml(encoding)

def getDirCommand(urls):
    """
    curl -sv refreshd  -d "<?xml version=\"1.0\" encoding=\"UTF-8\"?><method name=\"dir_purge\" purge_type=\"1\"
           sessionid=\"1\"><dir>dl.appstreaming.autodesk.com</dir></method>" -x  127.0.0.1:21108
    Args:
        urls:

    Returns:

    """
    physical_del_channel = str(0)
    if urls[0].get('physical_del_channel'):
        physical_del_channel = str(1)
    session_id = urls[0].get('id', uuid.uuid1().hex)
    action = 1 if (urls[0]['url'].find('*') > 0 or urls[0]['url'].find('?') > 0) else 0
    url = urls[0]
    if physical_del_channel == '0':

        if url.get('action') == 'purge':
            command = '<method name="dir_purge" sessionid="%s"><action>%d</action><dir>%s</dir><report_address>%s</report_address></method>' % (
                session_id, action, url['url'].lower() if url.get('ignore_case', False) else url['url'],
                config.get('server', 'report'))
        else:
            command = '<method name="dir_expire" sessionid="%s"><action>%d</action><dir>%s</dir><report_address>%s</report_address></method>' % (
                session_id, action, url['url'].lower() if url.get('ignore_case', False) else url['url'],
                config.get('server', 'report'))
    else:
        if url.get('action') == 'purge':
            command = '<method name="dir_purge" sessionid="%s" purge_type="%s"><action>%d</action><dir>%s</dir><report_address>%s</report_address></method>' % (
                session_id, physical_del_channel,action, url['url'].lower() if url.get('ignore_case', False) else url['url'],
                config.get('server', 'report'))
        else:
            command = '<method name="dir_expire" sessionid="%s" purge_type="%s"><action>%d</action><dir>%s</dir><report_address>%s</report_address></method>' % (
                session_id, physical_del_channel,action, url['url'].lower() if url.get('ignore_case', False) else url['url'],
                config.get('server', 'report'))
    return session_id, command.encode("UTF-8")

def check_physical_channel(url):
    s = url.split('/', 3)
    channelname = s[0] + '//' + s[2]
    if REWRITE_CACHE.exists('physical_del_channel_' + channelname):
        return True
    else:
        return False



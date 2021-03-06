# -*- coding:utf-8 -*-
"""
Created on 2011-5-31

@author: wenwen
"""
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import httplib2 as httplib
import uuid, asyncore, traceback, datetime, time
from xml.dom.minidom import parseString
import logging
from asyncpostal import HttpClient, HttpClient_test

import redisfactory
from database import db_session
from config import config
from models import STATUS_NOT_OPEN, STATUS_CONNECT_FAILED, STATUS_SUCCESS
from util import log_utils
import requests



DIR_COMMAND_EXPIRE = 12 * 3600
RETRY_DELAY_TIME = int(config.get("retry", "delay_time"))
RETRY_COUNT = int(config.get("retry", "count"))
blackListDB = redisfactory.getDB(1)
# logger = logging.getLogger('postal')
# logger.setLevel(logging.DEBUG)
logger = log_utils.get_postal_Logger()

MESSAGE_HOST = config.get("message_server", "host")
MESSAGE_PORT = config.get("message_server", "port")


def do_send_url(urls, devs):
    """
     下发URL到FC
    :param urls:
    :param devs:
    :return:
    """
    logger.debug(
        'do_send_url STARTING. dev_id:%s , urls_count:%s,devs_count:%s' % (urls[0].get("dev_id"), len(urls), len(devs)))
    # 找出设备中开着的设备，  关闭的设备，   黑名单设备
    dev_map, closed_devs, black_list_devs = getDevMapGroupByStatus(devs, urls)
    # 按接口格式，格式化url
    command = getUrlCommand(urls)
    ret, ret_faild = doloop(dev_map.values(), command)
    results, error_result = process_loop_ret(ret, dev_map, "url_ret")
    results_faild_dic = process_loop_ret_faild(ret_faild, dev_map)
    logger.debug('url doloop FINISHED.dev_id:%s , results count:%s,dev_map count:%s' % (
        urls[0].get("dev_id"), len(results), len(dev_map)))
    retry_devs = black_list_devs + dev_map.values()
    if retry_devs:
        logger.debug('retry STARTING! dev_id:%s ,retry_devs count:%s' % (urls[0].get("dev_id"), len(retry_devs)))
        try:
            results_faild_dic.update(error_result)
            retry_results = retry(retry_devs, command, "url_ret", results_faild_dic)
        except Exception,ex:
            logger.error(traceback.format_exc(ex))
        logger.debug('retry FINISHED! dev_id:%s ,retry_results count:%s' % (urls[0].get("dev_id"), len(retry_results)))
        results += retry_results
        # save_retry_failure_devs(urls, retry_devs, retry_results) #223.202.52.138 设备裁撤了
    for dev in closed_devs:
        results.append(getPostStatus(dev, STATUS_NOT_OPEN))
    logger.debug('do_send_url FINISHED. dev_id:%s , results count:%s !' % (urls[0].get("dev_id"), len(results)))
    return results


def do_send_dir(url, devs):
    logger.debug('do_send_dir STARTING.dev_id:%s , devs_count:%s' % (url.get("dev_id"), len(devs)))
    dev_map, closed_devs, black_list_devs = getDevMapGroupByStatus(devs, [url])
    session_id, command = getDirCommand([url])
    ret, ret_faild = doloop(dev_map.values(), command)
    results, error_result = process_loop_ret(ret, dev_map, "ret")
    results_faild_dic = process_loop_ret_faild(ret_faild, dev_map)
    logger.debug('dir doloop FINISHED .dev_id:%s , results count:%s,dev_map count:%s' % (
        url.get("dev_id"), len(results), len(dev_map)))
    retry_devs = black_list_devs + dev_map.values()
    if retry_devs:
        logger.debug('retry STARTING! dev_id:%s ,retry_devs count:%s' % (url.get("dev_id"), len(retry_devs)))
        try:
            results_faild_dic.update(error_result)
            retry_results = retry(retry_devs, command, "ret", results_faild_dic)
        except Exception,ex:
            logger.error(traceback.format_exc(ex))
        logger.debug('retry FINISHED! dev_id:%s ,retry_results count:%s' % (url.get("dev_id"), len(retry_results)))
        results += retry_results
        # save_retry_failure_devs([url], retry_devs, retry_results) #223.202.52.138 设备裁撤了
    for dev in closed_devs:
        results.append(getPostStatus(dev, STATUS_NOT_OPEN))
    logger.debug('do_send_dir FINISHED. dev_id:%s , results count:%s !' % (url.get("dev_id"), len(results)))
    return results


def retry(devs, command, node_name, results_faild_dic):
    ret_map = {}
    connect_timeout = 2
    response_timeout = 10
    for dev in devs:
        try:
            ret_map.setdefault(dev.get("host"), results_faild_dic[dev.get("host")])
        except Exception,ex:
            logger.debug('retry dev error:{0},{1}'.format(dev.get("host"),results_faild_dic))

    for retry_count in range(RETRY_COUNT):
        time.sleep(RETRY_DELAY_TIME)

        ret, ret_faild = doloop(devs, command, connect_timeout, response_timeout)

        for result in ret:
            try:
                host, xml_body, a_code, total_cost, connect_cost, response_cost = result.split('\r\n')
            except Exception, e:
                logger.error("%s response error result: %s" % (host, result))
            try:
                ret_map.get(host)["code"] = getCodeFromXml(xml_body, node_name)
                ret_map.get(host)["connect_cost"] = connect_cost
                ret_map.get(host)["response_cost"] = response_cost
                ret_map.get(host)["total_cost"] = total_cost
                ret_map.get(host)["r_code"] = int(a_code)
                ret_map.get(host)["times"] = 1
                # logger.debug("host_test1:%s, code_test1:%s, r_code_test1:%s" % (host, xml_body, a_code))
            except Exception, e:
                logger.error("%s response error xml_body: %s" % (host, xml_body))
                logger.error(traceback.format_exc(e))

        for w in ret_faild:
            try:
                host, a_code, total_cost, connect_cost, response_cost = w.split('\r\n')
            except Exception, e:
                logger.error("%s response error result: %s" % (host, w))
            try:
                ret_map.get(host)["connect_cost"] = connect_cost
                ret_map.get(host)["response_cost"] = response_cost
                ret_map.get(host)["total_cost"] = total_cost
                ret_map.get(host)["r_code"] = int(a_code)
                ret_map.get(host)["times"] = 1
                # logger.debug("host_test2:%s, r_code_test2:%s" % (host, a_code))
            except Exception, e:
                logger.error("%s response error xml_body: %s" % (host, xml_body))
                logger.error(traceback.format_exc(e))
            # results, error_result = process_loop_ret(ret, devs, node_name)
            # results_faild_dic = process_loop_ret_faild(ret_faild, devs)
            # results_faild_dic.update(error_result)

        # if retry_send(ret_map, command, node_name):
        #     break
    return ret_map.values()




def retry_send(ret_map, command, node_name):
    """
    失败后重新发送命令,不采用asyncore发送
    :param ret_map:
    :param command:
    :param node_name:
    :return:
    """
    devs = [dev for dev in ret_map.values() if dev.get("code") == STATUS_CONNECT_FAILED]
    ret, wrongRet = doSend_HTTP_Req(devs, command)
    for result in ret:
        try:
            host, xml_body,total_cost = result.split('\r\n')
        except Exception, e:
            logger.error("%s response error result: %s" % (host, result))
        try:
            ret_map.get(host)["code"] = getCodeFromXml(xml_body, node_name)
            ret_map.get(host)["r_cost"] = total_cost
            ret_map.get(host)["r_code"] = STATUS_SUCCESS
        except Exception, e:
            logger.error("%s response error xml_body: %s" % (host, xml_body))
            logger.error(traceback.format_exc(e))
    for w in wrongRet:
        try:
            host, r_code, total_cost = w.split('\r\n')
        except Exception, e:
            logger.error("%s response error result: %s" % (host, w))
        try:
            ret_map.get(host)["r_cost"] = total_cost
            ret_map.get(host)["r_code"] = int(r_code)
        except Exception, e:
            logger.error("%s response error xml_body: %s" % (host, xml_body))
            logger.error(traceback.format_exc(e))
    if len(devs) == len(ret):
        return True


def process_loop_ret_faild(ret,dev_map):
    """
    处理发送给FC后，失败的设备文档内容
    :param ret:
    :return:
    """
    results = {}
    for result in ret:
        host, a_code, total_cost, connect_cost, response_cost = result.split('\r\n')
        dev = dev_map.pop(host)
        try:
            results[host] = getPostStatus(dev, STATUS_CONNECT_FAILED, total_cost, connect_cost, response_cost, int(a_code))
            dev_map.setdefault(host, dev)
        except Exception, e:
            dev_map.setdefault(host, dev)
            logger.error(traceback.format_exc(e))
    return results

def process_loop_ret(ret, dev_map, node_name):
    """
    处理发送给FC后，FC返回的XML结果
    :param ret:['121.63.247.151\r\n<?xml version="1.0" encoding="UTF-8"?>\n<url_purge_response sessionid="7844e960e40b11e4a74900e0ed25a740">\n<url_ret id="0">200</url_ret>\n</url_purge_response>\r\n0\r\n0\r\n0']
    :param dev_map:
    :param node_name:
    :return:
    """
    results = []
    error_result = {}
    for result in ret:
        try:
            host, xml_body, a_code, total_cost, connect_cost, response_cost = result.split('\r\n')
            dev = dev_map.pop(host)
        except Exception, e:
            logger.debug("process_loop_ret result has problem:%s, error:%s" % (result, e))
            host, str_temp = result.split('\r\n', 1)
            dev = dev_map.pop(host)
            results.append(getPostStatus(dev, 0, 0, 0, 0, 0, 0))
            continue
        try:
            has_error = False
            for node in parseString(xml_body).getElementsByTagName(node_name):
                if node.firstChild.data == '404' or node.firstChild.data == '408':
                    dev_map.setdefault(host, dev)
                    has_error = True
                    error_result[host] = getPostStatus(dev, int(node.firstChild.data), total_cost, connect_cost, response_cost, int(a_code))
                    logger.error("%s response error,code: %s" % (host, node.firstChild.data))
                    break
            if not has_error:
                results.append(
                    getPostStatus(dev, getCodeFromXml(xml_body, node_name), total_cost, connect_cost, response_cost, int(a_code)))
        except Exception, e:
            dev_map.setdefault(host, dev)
            error_result[host] = getPostStatus(dev, STATUS_CONNECT_FAILED, total_cost, connect_cost, response_cost, int(a_code))
            logger.error("%s response error,%s: %s" % (host, len(xml_body), xml_body))
            logger.error(traceback.format_exc(e))
    return results, error_result


def save_retry_failure_devs(urls, retry_devs, retry_results):
    failure_results = [dev for dev in retry_results if dev.get("code") != STATUS_SUCCESS]
    if failure_results:
        try:
            start_time = time.time()
            rc = requests.post("http://%s:%d" % (MESSAGE_HOST, int(MESSAGE_PORT)), data=failure_results, timeout=(1, 2))#connect_timeout 1s reponse_timeout 2s
            rc.raise_for_status()
            logger.debug('send failure time: {0}'.format(time.time()-start_time))
        except Exception, ex:
            logger.debug('send failure error: {0}'.format((time.time()-start_time)))
    # failure_devs = [dev for dev in retry_devs if dev.get("name") in failure_results]
    # if failure_devs:
    #     save_error_task(urls,failure_devs,"STATUS_CONNECT_FAILED")


def save_error_task(urls, failure_devs, wrong_ret):
    """
    保存失败的信息到数据库
    :param urls:
    :param failure_devs:
    :param wrong_ret:
    """
    # return  # 暂时不记录错误信息
    errortask_list = []
    for dev in failure_devs:
        errortask_list.append({'urls': urls, "dev_id": urls[0].get("dev_id"), "host": dev.get('host'),
                               'created_time': datetime.datetime.now(), 'name': dev.get('name'),
                               'status': dev.get('status'), "wrongRet": wrong_ret})
    db_session().error_task.insert(errortask_list)


def getCodeFromXml(xmlBody, node_name):
    node = parseString(xmlBody).getElementsByTagName(node_name)[0]
    return int(node.firstChild.data)


def getPostStatus(dev, statusCode, total_cost=0, connect_cost=0, response_cost=0, a_code=200, r_code=200):
    return {"host": dev.get('host'), "firstLayer": dev.get('firstLayer'),
            "name": dev.get('name'), "code": statusCode, "total_cost": total_cost, "connect_cost": connect_cost,
            "response_cost": response_cost, "a_code": a_code, "r_code": r_code, "times": 0}


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
            if c.strerror != 'no_error':
                blackListDB.set(c.host, c.strerror)
                blackListDB.expire(c.host, 300)
    return ret, ret_faild


def doSend_HTTP(devs, command):
    """
     重试时直接用httplib发送，会增加一个返回码的判断
    :param devs:
    :param command:
    :return:
    """
    results = []
    wrongRet = []
    hc = httplib.Http(timeout=4)
    for dev in devs:
        try:
            start_time = time.time()
            response_body = ''
            repo, response_body = hc.request("http://%s:%d" % (dev['host'], 21108), method='POST', body=command)
            total_cost = (time.time() - start_time) * 1000
            if repo.status == 200:
                results.append(dev['host'] + '\r\n' + response_body + '\r\n%d\r\n%d\r\n%d' % (total_cost, 0, 0))
            else:
                wrongRet.append(dev['host'] + '\r\n' + response_body + '\r\n%d\r\n%d\r\n%d' % (total_cost, 0, 0))
                logger.error('%s post error. error code: %d' % (dev['host'], repo.status))
        except Exception, e:
            logger.error("%s connect error." % dev.get('host'))
            logger.error("response_body : %s connect error :%s ." % (response_body,traceback.format_exc(e)))
            wrongRet.append(str(e))
    return results, wrongRet


def doSend_HTTP_Req(devs, command):
    """
     重试时直接用requests发送，会增加一个返回码的判断
    :param devs:
    :param command:
    :return:
    """
    results = []
    wrongRet = []
    for dev in devs:
        r_code = 200
        total_cost = 0
        try:
            start_time = time.time()
            rc = requests.post("http://%s:%d" % (dev['host'], 21108), data=command, timeout=(2, 10))#connect_timeout 2s reponse_timeout 5s
            rc.raise_for_status()

            response_body = rc.text
            total_cost = time.time() - start_time

            results.append(dev['host'] + '\r\n' + response_body + '\r\n%.2f' % (total_cost))

        except requests.ConnectionError as e:
            r_code = 503
            total_cost = time.time() - start_time
            wrongRet.append(dev['host'] + '\r\n%d\r\n%.2f' % (r_code, total_cost))
        except requests.Timeout:
            r_code = 501
            total_cost = time.time() - start_time
            wrongRet.append(dev['host'] + '\r\n%d\r\n%.2f' % (r_code, total_cost))
        except Exception, e:
            r_code = 502
            total_cost = time.time() - start_time
            wrongRet.append(dev['host'] + '\r\n%d\r\n%.2f' % (r_code, total_cost))
            logger.error("%s connect error." % dev.get('host'))
            logger.error("connect error :%s ." % (traceback.format_exc(e)))
        logger.debug('retry %s  r_code: %d r_cost: %.2f' % (dev['host'], r_code, total_cost))
    return results, wrongRet


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
    if urls[0].get('url_encoding') and (len(urls) == 1):
        encoding = urls[0].get('url_encoding')
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
        #uelement.setAttribute('id', str(idx))
        uelement.setAttribute('id', url.get("id", str(idx))) #store url.id  in id
        logger.debug("send url.id:%s" % url.get("id"))
        # rubin test start
        # qurl = qurl.decode('utf8')
        # qurl = qurl.encode('gb2312')
        # rubin test end
        uelement.appendChild(content.createTextNode(qurl))
        url_list.documentElement.appendChild(uelement)
        tmp[url.get("url")] = ''
    content.documentElement.appendChild(url_list.documentElement)
    return content.toxml(encoding)
    # rubin test start
    # return content.toxml('gb2312')
    # rubin test end

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


def getDevMapGroupByStatus(devs, urls):
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
    # [dev_map.setdefault(d.get('host'), d) for d in devs if
    #  d.get('status') == 'OPEN' and not blackListDB.exists(d.get('host'))]
    [dev_map.setdefault(d.get('host'), d) for d in devs if d.get('status') == 'OPEN' ]
    closedDevices = [d for d in devs if d.get('status') != 'OPEN']
    # if closedDevices:
    # save_error_task(urls,closedDevices,"NotOpen!")
    # blackListDevices = [d for d in devs if blackListDB.exists(d.get('host'))]
    blackListDevices = []
    return dev_map, closedDevices, blackListDevices



def doloop_test(devs, commands, connect_timeout=1.5, response_timeout=1.5):
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
    port = 80
    for command in commands:
        clients.append(HttpClient_test(devs['host'], port, command, len(devs) * 200, my_map, connect_timeout,response_timeout))
    logger.debug('doloop_test LOOP STARTING.')

    asyncore.loop(timeout=0.1, map=my_map)

    logger.debug('doloop_test LOOP DONE.')
    for c in clients:
        response_body, total_cost, connect_cost, response_cost, response_code = c.read_buffer.getvalue(), c.total_cost, c.connect_cost, c.response_cost, c.response_code
        if response_body:
            try:
                ret.append(c.host + '\r\n' + response_body.split('\r\n\r\n')[1] + '\r\n%d\r\n%.2f\r\n%.2f\r\n%.2f' % (
                    response_code, total_cost, connect_cost, response_cost))
                # logger.warn("devs: %s doloop response_body: %s" % (devs, response_body))
                logger.debug("doloop_test have response_body host:%s, response_code:%s, response_body:%s" % (c.host, response_code, response_body))
            except Exception, e:
                # logger.error("devs: %s doloop response_body error: %s" % (devs, response_body))
                logger.error("doloop_test doloop error: %s" % traceback.format_exc(e))
        else:
            logger.debug("doloop_test not have response_body host:%s, response_code:%s" % (c.host, response_code))
            ret_faild.append(c.host + '\r\n%d\r\n%.2f\r\n%.2f\r\n%.2f' % (
                    response_code, total_cost, connect_cost, response_cost))
            if c.strerror != 'no_error':
                blackListDB.set(c.host, c.strerror)
                blackListDB.expire(c.host, 300)
    return ret, ret_faild


def test_request():
    """

    Returns:

    """

    devs = {'host': "223.202.201.161"}
    url = ['http://download2.game.yy.com/1K.txt']

    for i in range(11):
        temp = {}
        temp['action'] = "purge"
        temp['url'] = 'http://download2.game.yy.com/1K.txt' + "." + str(i)
        url.append(temp['url'])
    commands = url
    while(1):
        time.sleep(0.1)
        doloop_test(devs, commands, connect_timeout=1.5, response_timeout=1.5)


def doloop_test_send(devs, url, connect_timeout=1.5, response_timeout=1.5):
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
        command = getUrlCommand(url)
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
            if c.strerror != 'no_error':
                blackListDB.set(c.host, c.strerror)
                blackListDB.expire(c.host, 300)
    return ret, ret_faild


def test_refresh():
    """

    Returns:

    """
    # 变量
    # url  数量
    url_count = 12
    # 每次并发链接数
    bingfa_count = 50
    # 发送次数
    send_count = 999


    url = [{"action": 'purge', 'url': 'http://download2.game.yy.com/1K.txt'}]

    for i in range(url_count -1):
        temp = {}
        temp['action'] = "purge"
        temp['url'] = 'http://download2.game.yy.com/1K.txt' + "." + str(i)
        url.append(temp)

    dev = []

    for i in range(bingfa_count):
        dev.append({'host': '223.202.201.161', 'name': 'CHN-WX-c-3WB'})

    count_501 = 0
    count_200 = 0
    count_503 = 0
    error_count = 0
    failed_count = 0
    start_time = time.time()
    i_t = 0
    for i in range(send_count):
        i_t += 1
        print "i_t:%s" % i_t
        time.sleep(0.1)
        # command = getUrlCommand(url)
        ret, ret_faild = doloop_test_send(dev, url)
        print 'i:%s, ret:%s' %(i, ret)
        try:
            for ret_t in ret:
                host, xml_body, a_code, total_cost, connect_cost, response_cost = ret_t.split('\r\n')
                # print "type a_code:%s" % type(a_code)
                if a_code == '501':
                    count_501 += 1
                if a_code == '200':
                    count_200 += 1
                if a_code == '503':
                    count_503 += 1
            for ret_faild_t in ret_faild:
                failed_count += 1

        except Exception, e:
            print "logs error:%s" % traceback.format_exc(e)
            error_count += 1
            continue
        print 'i:%s, ret_faild:%s' %(i, ret_faild)
    end_time = time.time()

    print "chazhi :%s" % (end_time - start_time)
    logger.debug("chazhi :%s" % (end_time - start_time))
    print "time start:%s" % start_time
    logger.debug("time start:%s" % start_time)
    print "end　start:%s" % end_time
    logger.debug("end　start:%s" % end_time)

    print "count_501:%s" % count_501
    logger.debug("count_501:%s" % count_501)
    print "count_200:%s" % count_200
    logger.debug("count_200:%s" % count_200)
    print "count_503:%s" % count_503
    logger.debug("count_503:%s" % count_503)
    print "all number:%s" % str(url_count * bingfa_count * send_count)
    logger.debug("all number:%s" % str(url_count * bingfa_count * send_count))
    print "send url number:%s" % (url_count * bingfa_count * send_count - failed_count * bingfa_count * send_count)
    logger.debug("send url number:%s" % (url_count * bingfa_count * send_count - failed_count * bingfa_count * send_count))
    print "error task :%s" % error_count
    logger.debug("error task :%s" % error_count)


if __name__ == "__main__":
    test_refresh()









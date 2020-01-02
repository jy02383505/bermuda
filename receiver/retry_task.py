#!/usr/bin/env python
# coding=utf-8
# Created by vance on 2015-03-09.

__author__ = 'vance'

from flask import Blueprint, request, make_response, jsonify
from core import database, postal, rcmsapi
from bson import ObjectId
import datetime
import traceback
from util import log_utils
from celery.task import task
from util.check_error_url import get_fail_url_device
import json
from bson.objectid import ObjectId
retry = Blueprint('retry', __name__, )
query_db_session = database.query_db_session()
db_session = database.db_session()
logger = log_utils.get_celery_Logger()

@retry.route("/internal/retry_user", methods=['GET', 'POST'])
def retry_user():
    try:
        result = {}
        logger.info(request.data)
        query_args = json.loads(request.data)
        logger.info(query_args)
        query_type = query_args.get('query_type')
        if query_type == 'normal_query':
            dt =datetime.datetime.strptime(query_args.get("date"), "%m/%d/%Y")
            query = {'created_time':{"$gte":dt, "$lt":(dt + datetime.timedelta(days=1))}}
        else:
            start_datetime =datetime.datetime.strptime(query_args.get("start_datetime"), "%Y-%m-%d %H")
            end_datetime = datetime.datetime.strptime(query_args.get("end_datetime"), "%Y-%m-%d %H")
            query = {'created_time':{"$gte":start_datetime, "$lt": end_datetime}}
        if query_args.get("username"):
            append_userfield(query_args.get("username"),query)
        #query['status']={"$ne":"FINISHED"}
        query['status']="FAILED"
        logger.info(query)
        dev_list=db_session.url.aggregate([{'$match':query},{'$group' : {'_id' : "$dev_id"}}])
        dev_list=list(dev_list)
        logger.info(dev_list)
        for dev_id in dev_list:
            dev_id=dev_id['_id']
            query['dev_id']=dev_id
            urls_list=db_session.url.find(query)

            dir_url_list=[]
            no_dir_url_list=[]
            for url_u in urls_list:
                if url_u['isdir']==True:
                    dir_url_list.append(url_u['_id'])
                else:
                    no_dir_url_list.append(url_u['_id'])

            for url_dir in dir_url_list:
                retry_task_urls([url_dir])
            if len(no_dir_url_list)>0:
                retry_task_urls(no_dir_url_list)
        result["code"] = 200
        result["message"] = 'ok'
        return jsonify(result)
    except Exception, ex:
        logger.debug("retry error:%s" % traceback.format_exc(ex))
        return jsonify({"code": 500, "message": "retry faild"})
@retry.route("/internal/page_retry", methods=['GET', 'POST'])
def page_retry():
    try:
        result = {}
        logger.info(request.data)
        query_args = json.loads(request.data)
        logger.info(query_args)
        strurl=query_args.get('strurl')
        urls=strurl.split(',')
        retrydict={}
        dirList=[]
        for urlid in urls:
            url=db_session.url.find_one({"_id": ObjectId(urlid)})
            if url.get('isdir'):
                dirList.append(ObjectId(urlid))
            else:
                retrydict.setdefault(url.get('dev_id'), []).append(ObjectId(urlid))
        for urldir in dirList:
            retry_task_urls([urldir])
        for keys in retrydict.keys():
            retry_task_urls(retrydict.get(keys))
        result["code"] = 200
        result["message"] = 'ok'
        return jsonify(result)
    except Exception, ex:
        logger.debug("retry error:%s" % traceback.format_exc(ex))
        return jsonify({"code": 500, "message": "retry faild"})

def append_userfield(username,query):
    from cache import rediscache
    if rediscache.isFunctionUser(username):
        query['username']=username
    else:
        query['parent'] = username

@retry.route("/internal/retry/<uid>", methods=['GET'])
def retry_task(uid):
    """

    :param uid:
    :return:
    code  message
    200    ok
    404    Not found uid
    500    retry faild
    """
    try:
        logger.debug("get retry task uid {0}".format(uid))
        result = {}
        db_request = query_db_session.ref_err.find_one({"uid": ObjectId(uid)})
        if db_request:
            # queue.put_json2("retry_task", (uid,))
            if "retry_success" not in db_request:
                retry_worker.delay((uid,))
            else:
                logger.debug("get retry task uid {0} is success".format(uid))
            result["code"] = 200
            result["message"] = 'ok'
        else:
            if sync_ref_err(uid):
                # queue.put_json2("retry_task", (uid,))
                retry_worker.delay((uid,))
                result["code"] = 200
                result["message"] = 'ok'
            else:
                result["code"] = 404
                result["message"] = 'Not found uid {0}'.format(uid)
        logger.debug("finish retry task uid {0}".format(uid))
        return jsonify(result)
    except Exception, ex:
        logger.debug("retry error:%s" % traceback.format_exc(ex))
        return jsonify({"code": 500, "message": "retry faild"})


def sync_ref_err(uid):
    u_dic = get_fail_urls(uid)
    if u_dic:
        try:
            db_session.ref_err.insert(u_dic)
            return True
        except Exception, ex:
            logger.debug("internal_search_task error:%s" % traceback.format_exc(ex))
            return False
    else:
        return False


def get_fail_urls(uid):
    obj_url = query_db_session.url.find_one({"_id": ObjectId(uid)})
    if obj_url:
        u_dic = {}
        create_date = obj_url["created_time"]
        date = datetime.datetime.combine(create_date.date(),
                                         create_date.time().replace(minute=0, second=0, microsecond=0))
        u_dic['username'] = obj_url["parent"]  # 取主账户
        u_dic['uid'] = obj_url["_id"]
        u_dic['url'] = obj_url["url"]
        u_dic['channel_code'] = obj_url["channel_code"]
        u_dic['datetime'] = date
        u_dic['dev_id'] = obj_url["dev_id"]
        # u_dic['failed'], u_dic['f_devs'], u_dic['firstLayer'] = get_fail_url_device(obj_url["dev_id"])
        u_dic['failed'], u_dic['f_devs'], u_dic['firstLayer'], u_dic['devices'] = get_fail_url_device(query_db_session.device,obj_url["dev_id"])
        return u_dic
    else:
        return None




def get_url(uid):
    obj_url = query_db_session.url.find_one({"_id": ObjectId(uid)})
    if obj_url:
        return obj_url
    else:
        return None
def get_url_add_id(uid):
    obj_url = query_db_session.url.find_one({"_id": ObjectId(uid)})
    if obj_url:
        obj_url['id']=uid
        return obj_url
    else:
        return None


def get_rcms_devices(urls):
    devs_f = []
    devs = rcmsapi.getDevices(urls[0].get("channel_code"))
    dev_s = [dev['name'] for dev in devs if dev['status'] == 'OPEN']

    logger.debug('get_rcms_device:%s' % urls[0].get("layer_type"))
    if urls[0].get("is_multilayer"):
        devs_f = rcmsapi.getFirstLayerDevices(urls[0].get("channel_code"))
        devs_f = [dev['name'] for dev in devs_f if dev['status'] == 'OPEN']
    return dev_s, devs_f


def update_devices(dev_id, results):
    dev_obj = query_db_session.device.find_one({"_id": dev_id})
    fail_list = []
    for d in results:
        code = d['code']
        if code not in [200, 204]:
            fail_list.append(d['name'])
        dev_obj['devices'][d['name']]['code'] = code
        dev_obj['devices'][d['name']]['connect_cost'] = d['connect_cost']
        dev_obj['devices'][d['name']]['total_cost'] = d['total_cost']
        dev_obj['devices'][d['name']]['response_cost'] = d['response_cost']

    dev_obj["finish_time"] = datetime.datetime.now()
    db_session.device.save(dev_obj)
    return fail_list


def save_rey_devices(results):
    # TTL: db.retry_device.ensureIndex( { "finish_time": -1 }, { expireAfterSeconds: 60*60*24*7 })

    fail_list = [d['name'] for d in results["devices"] if d['code'] not in [200, 204]]

    results["finish_time"] = datetime.datetime.now()
    r_obj = db_session.retry_device.insert(results)

    return fail_list, r_obj

def update_url(uid, retry_obj, fail_list):
    url_obj = query_db_session.url.find_one({"_id": uid})
    url_obj["retry_time"] = datetime.datetime.now()
    try:
        url_obj["retrys"] += 1
        url_obj["r_dev_id"] = retry_obj
    except:
        url_obj["retrys"] = 1
        url_obj["r_dev_id"] = retry_obj

    logger.debug('fail_list %s'%fail_list)
    if not fail_list:
        url_obj["status"] = 'FINISHED'
        url_obj["retry_success"] = 1
        err_obj =query_db_session.ref_err.find_one({"uid": uid})
        err_obj["retry_success"] = 1
        db_session.ref_err.save(err_obj)
    else:
        url_obj["status"] = 'FAILED'

    db_session.url.save(url_obj)

#同一个设备组
def retry_task_urls(uids):
    """

    :param uid:
    :return:
    code  message
    200    ok
    404    Not found uid
    500    retry faild
    """
    logger.debug("get retry task uids {0}".format(uids))
    uid_list=[]
    for uid in uids:
        try:
            db_request = query_db_session.ref_err.find_one({"uid": uid})#找到url
            if db_request:
                # queue.put_json2("retry_task", (uid,))
                if "retry_success" not in db_request:
                    uid_list.append(uid)
                else:
                    logger.debug("get retry task uid {0} is success".format(uid))
            else:
                if sync_ref_err(str(uid)):#没有将url同步到ref_err中
                    # queue.put_json2("retry_task", (uid,))
                    uid_list.append(uid)
            #logger.debug("finish retry task uid {0}".format(uid))
        except Exception, ex:
            logger.debug("retry error:%s" % traceback.format_exc(ex))
    retry_new_work.delay((uid_list,))

@task(ignore_result=True, default_retry_delay=10, max_retries=3)
def retry_new_work(task):
    logger.info("retry worker get uids {0}".format(task[0]))
    devs_f = []
    devs = []
    devices = []
    results= {}
    dev_fail = []
    uid_list= task[0]
    isDir=False
    if len(uid_list)<1 :
        return
    elif len(uid_list)==1 :
        isDir=query_db_session.url.find_one({"_id": uid_list[0]})['isdir']

    urls=[]
    for uid in uid_list:
        urls.append(get_url_add_id(uid))
    db_ref_err = query_db_session.ref_err.find_one({"uid": uid_list[0]})   
    rcms_dev_s, rcms_dev_f = get_rcms_devices(urls)#根据url中的channels信息，从redis中寻找设备，redis中

    if db_ref_err['firstLayer']:
        devs_f = [{"name": k, "host": v, 'firstLayer': True, "status": "OPEN" if k in rcms_dev_f else "SUSPEND"} for k, v in
                  db_ref_err['f_devs'].items()]
    if isDir:
        logger.info("dir retry id list: %s"%uid_list)
        devices.extend(update_result(devs_f, postal.do_send_dir(urls[0], devs_f)))#保存设备，下发url
    else:
        devices.extend(update_result(devs_f, postal.do_send_url(urls, devs_f)))#保存设备，下发url
        
    logger.info("send first layer devs {0}".format(len(devs_f)))

    devs = [{"name": k, "host": v, 'firstLayer': False, "status": "OPEN" if k in rcms_dev_s else "SUSPEND"} for d in
            db_ref_err['failed'] for dd in d["devices"] for k, v in dd.items()]
    if devs:
        if isDir:
            devices.extend(update_result(devs, postal.do_send_dir(urls[0], devs)))
        else:
            devices.extend(update_result(devs, postal.do_send_url(urls, devs)))
        logger.debug(devices)
    results["devices"] = devices
    dev_fail, retry_obj = save_rey_devices(results)#保存重试device数据库
    for uid in uid_list :
    	update_url(ObjectId(uid), retry_obj, dev_fail)#保存url数据库，插入成功的数据，错误列表

    logger.info("send second layer devs {0}".format(len(devs)))

def update_result(devices,result):
     # [t1 if t1.update(t2) else t2 for t1 in aa for t2 in bb if t1['name']==t2['name']]
    # [dict(t1,**t2) for t1 in aa for t2 in bb if t1['name']==t2['name']]
    return [dict(dd, **re) for dd in devices for re in result if dd["name"] == re["name"]]


@task(ignore_result=True, default_retry_delay=10, max_retries=3)
def retry_worker(task):
    logger.info("retry worker get uid {0}".format(task[0]))
    uid = task[0]
    devs_f = []
    devs = []
    devices = []
    results= {}
    dev_fail = []
    results ={"created_time":datetime.datetime.now()}
    db_ref_err = query_db_session.ref_err.find_one({"uid": ObjectId(uid)})
    db_url = query_db_session.url.find_one({"_id": ObjectId(uid)})
    try:
        if db_ref_err:
            urls = [get_url(uid)]
            rcms_dev_s, rcms_dev_f = get_rcms_devices(urls)
            if db_ref_err['firstLayer']:
                devs_f = [{"name": k, "host": v, 'firstLayer': True, "status": "OPEN" if k in rcms_dev_f else "SUSPEND"} for k, v in
                          db_ref_err['f_devs'].items()]
                if db_url['isdir']:
                    devices.extend(update_result(devs_f, postal.do_send_dir(urls, devs_f)))
                else:
                    devices.extend(update_result(devs_f, postal.do_send_url(urls, devs_f)))

                logger.info("send first layer devs {0}".format(len(devs_f)))

            devs = [{"name": k, "host": v, 'firstLayer': False, "status": "OPEN" if k in rcms_dev_s else "SUSPEND"} for d in
                    db_ref_err['failed'] for dd in d["devices"] for k, v in dd.items()]
            if devs:
                if db_url['isdir']:
                    devices.extend(update_result(devs, postal.do_send_dir(urls, devs)))
                else:
                    devices.extend(update_result(devs, postal.do_send_url(urls, devs)))
                logger.debug(devices)
            results["devices"] = devices
            dev_fail, retry_obj = save_rey_devices(results)
            update_url(ObjectId(uid), retry_obj, dev_fail)

            logger.info("send second layer devs {0}".format(len(devs)))
    except Exception, ex:
        logger.info("retry worker get devices {0}".format(traceback.format_exc(ex)))

        # [{'code': 503, 'name': u'CHN-WX-b-3SE', 'total_cost': 0, 'connect_cost': 0, 'host': u'58.215.107.35', 'response_cost': 0, 'firstLayer': None}, {'code': 503, 'name': u'CHN-JG-2-3Se', 'total_cost': 0, 'connect_cost': 0, 'host': u'221.233.42.66', 'response_cost': 0, 'firstLayer': None}, {'code': 503, 'name': u'CHN-JG-2-3Sc', 'total_cost': 0, 'connect_cost': 0, 'host': u'221.233.42.64', 'response_cost': 0, 'firstLayer': None}, {'code': 503, 'name': u'CHN-JG-2-3SL', 'total_cost': 0, 'connect_cost': 0, 'host': u'221.233.42.47', 'response_cost': 0, 'firstLayer': None}, {'code': 503, 'name': u'CNC-CQ-2-3SG', 'total_cost': 0, 'connect_cost': 0, 'host': u'113.207.20.164', 'response_cost': 0, 'firstLayer': None}, {'code': 503, 'name': u'CHN-SX-2-3SO', 'total_cost': 0, 'connect_cost': 0, 'host': u'115.231.15.55', 'response_cost': 0, 'firstLayer': None}, {'code': 503, 'name': u'CHN-QX-f-3SG', 'total_cost': 0, 'connect_cost': 0, 'host': u'171.107.84.91', 'response_cost': 0, 'firstLayer': None}, {'code': 503, 'name': u'CNC-LQ-c-3WG', 'total_cost': 0, 'connect_cost': 0, 'host': u'61.240.135.199', 'response_cost': 0, 'firstLayer': None}, {'code': 503, 'name': u'CNC-XD-b-3W1', 'total_cost': 0, 'connect_cost': 0, 'host': u'221.204.21.2', 'response_cost': 0, 'firstLayer': None}, {'code': 503, 'name': u'CNC-CQ-2-3SO', 'total_cost': 0, 'connect_cost': 0, 'host': u'113.207.20.174', 'response_cost': 0, 'firstLayer': None}, {'code': 503, 'name': u'CHN-YN-b-3SV', 'total_cost': 0, 'connect_cost': 0, 'host': u'61.178.248.52', 'response_cost': 0, 'firstLayer': None}, {'code': 503, 'name': u'WAS-HZ-1-3dB', 'total_cost': 0, 'connect_cost': 0, 'host': u'113.215.1.202', 'response_cost': 0, 'firstLayer': None}]
        # [2015-03-17 16:20:23,199: DEBUG/MainProcess] [{'code': 503, 'name': u'CHN-WX-b-3SE', 'total_cost': 0, 'connect_cost': 0, 'host': u'58.215.107.35', 'response_cost': 0, 'firstLayer': None}, {'code': 503, 'name': u'CHN-JG-2-3Se', 'total_cost': 0, 'connect_cost': 0, 'host': u'221.233.42.66', 'response_cost': 0, 'firstLayer': None}, {'code': 503, 'name': u'CHN-JG-2-3Sc', 'total_cost': 0, 'connect_cost': 0, 'host': u'221.233.42.64', 'response_cost': 0, 'firstLayer': None}, {'code': 503, 'name': u'CHN-JG-2-3SL', 'total_cost': 0, 'connect_cost': 0, 'host': u'221.233.42.47', 'response_cost': 0, 'firstLayer': None}, {'code': 503, 'name': u'CNC-CQ-2-3SG', 'total_cost': 0, 'connect_cost': 0, 'host': u'113.207.20.164', 'response_cost': 0, 'firstLayer': None}, {'code': 503, 'name': u'CHN-SX-2-3SO', 'total_cost': 0, 'connect_cost': 0, 'host': u'115.231.15.55', 'response_cost': 0, 'firstLayer': None}, {'code': 503, 'name': u'CHN-QX-f-3SG', 'total_cost': 0, 'connect_cost': 0, 'host': u'171.107.84.91', 'response_cost': 0, 'firstLayer': None}, {'code': 503, 'name': u'CNC-LQ-c-3WG', 'total_cost': 0, 'connect_cost': 0, 'host': u'61.240.135.199', 'response_cost': 0, 'firstLayer': None}, {'code': 503, 'name': u'CNC-XD-b-3W1', 'total_cost': 0, 'connect_cost': 0, 'host': u'221.204.21.2', 'response_cost': 0, 'firstLayer': None}, {'code': 503, 'name': u'CNC-CQ-2-3SO', 'total_cost': 0, 'connect_cost': 0, 'host': u'113.207.20.174', 'response_cost': 0, 'firstLayer': None}, {'code': 503, 'name': u'CHN-YN-b-3SV', 'total_cost': 0, 'connect_cost': 0, 'host': u'61.178.248.52', 'response_cost': 0, 'firstLayer': None}, {'code': 503, 'name': u'WAS-HZ-1-3dB', 'total_cost': 0, 'connect_cost': 0, 'host': u'113.215.1.202', 'response_cost': 0, 'firstLayer': None}]


# -*- coding: UTF-8 -*-

from bson import ObjectId
from core.database import query_db_session, db_session, s1_db_session,multi_session
from core import redisfactory
import traceback
from util import log_utils
from core.config import config
from util.tools import get_mongo_str
import os
import gzip

from core import queue,models
import json
import pymongo
logger = log_utils.get_receiver_Logger()

db = db_session()
q_db = query_db_session()
monitor_db = s1_db_session()
multi_db = multi_session()
REWRITE_CACHE = redisfactory.getDB(15)


def get_url_by_id(id, url=False):
    """

    :param id: the id of url
    :return:
    """
    if not url:
        result = {}
        try:

            result = q_db.url.find_one({'_id': ObjectId(id)})
        except Exception, e:
            logger.debug('find url error:%s, id:%s' % (e, id))
        if result:
            dev_id = str(result.get('dev_id'))
            return dev_id
    else:
        result = {}
        try:

            result = q_db.url.find_one({'_id': ObjectId(id)})
        except Exception, e:
            logger.debug('find url error:%s, id:%s' % (e, id))
        if result:
            dev_id = str(result.get('dev_id'))
            url_t = str(result.get('url'))
            return {"dev_id": dev_id, "url": url_t}
    return None


def get_urls_by_request(request_id):
    url_list = [{'u_id': x.get('_id'), 'url': x.get('url'), 'dev_id': x.get('dev_id')} for x in
                q_db.url.find({'r_id': ObjectId(request_id)})]
    return url_list

def get_request_by_request(request_id):
    request_m = q_db.request.find_one({'_id': ObjectId(request_id)})
    return request_m

def get_repsql_by_chanelName(chanelName):
    rep = q_db.repsql.find_one({'chanelName': chanelName})
    return rep

def get_refresh_result_by_sessinId(session_id):
    """
    根据session_id，返回要查询的信息
    Parameters
    ----------
    session_id   refresh_result collection  中的session_id

    Returns   返回refresh_result中的信息
    -------
    """
    # session_id = '5b3c835637d015a9cd07d69e'

    logger.debug('action    sessid_id type is {0}'.format(type(session_id)))
    str_num = ''
    try:
        num_str = config.get('refresh_result', 'num')
        str_num = get_mongo_str(str(session_id), num_str)
    except Exception, e:
        logger.debug('get refresh_result get number of refresh_result error:%s' % traceback.format_exc(e))
    logger.debug('-------------session_id:{0},str_num:{1}'.format(session_id, str_num))
    logger.debug('sessid_id type is {0}'.format(type(session_id)))
    res = monitor_db['refresh_result' + str_num].find({'session_id': str(session_id)})
    # for x in res:
    #    logger.debug('-------------session_id:{0}'.format(x))
    if not res:
        return []
    else:
        # return assembel_refresh_result(res)
        return res


def get_devs_by_id(dev_id):
    return q_db.device.find_one({'_id': ObjectId(dev_id)})
def send_result_error(err_message):
    #err_message = {'request_id': request_id, 'url': url.get('url'), 'success': ss_count, 'all': countAll,'channelName': url.get('channel_name')}
    rep = q_db.rep_channel.find_one({'channelName': err_message.get('channelName')})
    to_user =rep.get('userName',None)
    if to_user:
        to_user =rep.get('userName').split(',')
    else:
        to_user = ["pengfei.hao@chinacache.com"]
    email = [{"username": to_user, "to_addrs": to_user,"title": u'刷新回调失败任务', "body": json.dumps(err_message)}]
    queue.put_json2('email',email)

def get_device_failed_url(hostname, start_datetime, end_datetime, channel_name=None, username_list=None):
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
    db_key = hash(hostname)%50
    db_name = "device_urls_day_{}".format(db_key)
    # return multi_db.device_urls_day.find(_query).sort('datetime', pymongo.ASCENDING)
    return multi_db[db_name].find(_query).sort('datetime', pymongo.ASCENDING)
def device_failed_url_to_txt(txt_name, res):
    '''
    设备任务生成txt
    '''
    #dir = '/Application/bermuda/static/log_txt/%s.txt' %(txt_name)
    z_dir = '/Application/bermuda/static/log_txt/%s.txt.gz' %(txt_name)
    if os.path.exists(z_dir):
        os.remove(z_dir)

    writes = make_failed_url_res(res)

    with gzip.open(z_dir, 'wb') as f:
        f.write('\n'.join(writes))

    return
def make_failed_url_res(res):
    '''
    生成边缘脚本执行格式内容
    '''
    writes = []

    #logger.debug(r.count())

    for r in res:
        _type = 'url'
        if r['url']['isdir']:
            _type = 'dir'
        # strs = '%s,%s,%s,%s' %(r['url']['url'], r['url']['action'],_type, r.get('datetime', ''))

        phy = '0'
        # if check_physical_channel(r['url']['url']):
        #     phy= '1'
        if r['url'].get('physical_del_channel',False):
            phy = '1'
        strs = '%s,%s,%s,%s,%s' %(r['url']['url'], r['url']['action'],_type, r.get('datetime', ''),phy)

        writes.append(strs.encode("utf-8"))
    return writes

def check_physical_channel(url):
    try:
        s = url.split('/', 3)
        channelname = s[0] + '//' + s[2]
        if REWRITE_CACHE.exists('physical_del_channel_' + channelname):
            return True
        else:
            return False
    except Exception,ex:
        return False

def change_pull_time(hostname,pull_time):
    monitor_db.device_status_change.insert({"hostname": hostname, "status": "PULL", "datetime": pull_time})


def get_start_pull_time(hostname):
    last_time = None
    d_last_data =monitor_db.device_status_change.find({"hostname": hostname, "status": {"$in":["CLOSED", "SUSPEND", "PULL", "PUSH"]}}).sort('datetime', pymongo.DESCENDING)
    for dc in d_last_data:
        last_time = dc.get("datetime")
        break
    if last_time:
        return last_time
    else:
        return None

def get_start_pull_time_back(hostname):
    # get pull time or suspendtime
    d_close_time, d_open_time, d_pull_time, d_push_time = None, None, None, None
    d_close =monitor_db.device_status_change.find({"hostname": hostname, "status": {"$in":["CLOSED", "SUSPEND"]}}).sort('datetime', pymongo.ASCENDING)
    for dc in d_close:
        d_close_time = dc.get("datetime")
        break
    # open --> push
    # d_open = monitor_db.device_status_change.find({"hostname": hostname, "status": "OPEN"}).sort('datetime', pymongo.ASCENDING)
    # for do in d_open:
    #     d_open_time = do.get("datetime")
    #     break

    d_pull = monitor_db.device_status_change.find({"hostname": hostname, "status": "PULL"}).sort('datetime', pymongo.ASCENDING)
    for dp in d_pull:
        d_pull_time = dp.get("datetime")
        break

    d_push = monitor_db.device_status_change.find({"hostname": hostname, "status": "PUSH"}).sort('datetime', pymongo.ASCENDING)
    for dps in d_push:
        d_push_time = dps.get("datetime")
        break

    time_list = [n for n in [d_close_time, d_pull_time, d_push_time] if n]
    # time_list = [n for n in [d_pull_time, d_push_time] if n]
    if len(time_list) > 0:
        return max(time_list)
    return None





if __name__ == "__main__":
    print  get_refresh_result_by_sessinId('5b3de57737d0155f543d7272')
    print  get_request_by_request('5b3de57737d0155f543d7272')



#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by vance on 8/8/14.
import copy

__author__ = 'vance'
__doc__ = """
    测试脚本，转发正式环境下的任务，批量测试服务器接收处理能力，生成两个日志文件；
    transfer_url.log:发送内容的记录日志
    trans_url.log:处理能力的记录日志


    Start Time:2014-12-03 11:22:16                      开始时间
    send to:http://101.251.97.251/content/refresh       发送接口
    send total urls: 10                                 发送条数
    create process:5                                    创建进程数
    code:num
    200:6                                               返回状态码及相应次数（也可以体现出发送的包数，同一用户放一个包）
    500:1
    error list:                                          错误列表
    total time:0:00:02.289800                            耗时

"""
__ver__ = '1.0'

import urllib
import logging
import sys
from core import database
import multiprocessing
import simplejson as json
import string
import datetime
import collections

reload(sys)
sys.setdefaultencoding('utf8')

LOG_FILENAME = '/Application/bermuda/logs/transfer_url.log'
COUNT_LOG_FILENAME = '/Application/bermuda/logs/trans_url.log'
logging.basicConfig(filename=LOG_FILENAME,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(process)d - Line:%(lineno)d - %(message)s',
                    level=logging.INFO)
# SEND_URL = "http://101.251.97.251/internal/refresh"
SEND_URL_LIST = ["http://101.251.97.251/content/refresh", "http://101.251.97.214/content/refresh"]

LIMIT = 10
logger = logging.getLogger('transfer_url')
logger.setLevel(logging.DEBUG)
BATCH_SIZE = 2
STRLEN = 18
db = database.query_db_session()
json_file = "/Application/bermuda/user.json"
fail_queue = multiprocessing.Queue()
code_queue = multiprocessing.Queue()


def write_count_log(content):
    log_file = COUNT_LOG_FILENAME
    f = file("%s" % log_file, "a")
    f.write(str(content) + "\r\n")
    f.flush()
    f.close()


def process_return(code, content):
    try:
        co = json.loads(content)
        if "error_urls" in co.keys():
            fail_queue.put(co["error_urls"])
    except Exception, ex:
        logger.debug(ex)
        logger.debug(content)
        co = content
    code_queue.put(code)

    return code, content


def do_post(query, user_dic, send_url):
    """
    发送任务
    :param query: 结果集
    :param user_dic: 用户字典
    """
    username_dic = {}
    logger.debug('process to :%s ' % (query.count(True)))
    for u in query:
        if u['username'] not in user_dic.keys():
            logger.debug('{0} not in user.json'.format(u['username']))
            fail_queue.put(u['url'])
            continue
        if u['username'] not in username_dic.keys():
            username_dic[u['username']] = ["%s" % u['url']]
        else:
            url_list = username_dic[u['username']]
            if len(url_list) < 100:
                url_list.append("%s" % u['url'])
                username_dic[u['username']] = url_list
            else:
                logger.debug('send to :%s ' % (len(username_dic[u['username']])))
                logger.debug(username_dic[u['username']])
                params = urllib.urlencode({'username': u['username'],
                                           'password': user_dic[u['username'].encode('utf8')],
                                           'isSub': 'True',
                                           'task': '{"urls":["%s"]}' % '","'.join(username_dic[u['username']])})
                f = urllib.urlopen(send_url, params)
                # logger.debug(params)
                logger.debug(process_return(f.code, f.read()))
                username_dic.pop(u['username'])
    for key, value in username_dic.items():
        logger.debug('send to {0}'.format(len(value)))
        logger.debug(value)
        params = urllib.urlencode({'username': key, 'password': user_dic[key.encode('utf8')], 'isSub': 'True',
                                   'task': '{"urls":["%s"]}' % '","'.join(value)})
        # logger.debug(params)
        f = urllib.urlopen(send_url, params)
        logger.debug(process_return(f.code, f.read()))


def format_string(sstrs):
    return string.ljust(sstrs, STRLEN)


class Transfer(object):
    def __init__(self, collection, limit, filter):
        self.collection = collection
        self.limit = limit
        self.filter = filter
        self.querys = ''
        # self.end_date = datetime.datetime.combine(end_date, datetime.time())
        self.u_dic = {}
        self.user_dic = {}


    def get_users(self):
        """
        读取JSON文件内的用户

        """
        with open(json_file, 'r+') as f_user:
            self.user_dic = json.loads(f_user.read())
            # print USER_DIC

    def get_urls(self):
        """
        获取URLS

        """
        logger.debug('get task :%s ' % (self.limit))
        self.querys = self.collection.find({}, {'username': 1, 'url': 1, '_id': 0}).sort("created_time", -1).limit(
            self.limit)

    def merg_urls(self):
        pass

    def send_url(self, send_url):
        """
        发送任务到指定的URL
        :param send_url: 指定的URL
        """
        username_dic = {}  # 合并任务包，一个包不超过100条url
        # print dir(self.querys)
        querys = copy.copy(self.querys)
        self.code_dic = collections.defaultdict(int)
        print id(self.querys)
        print id(querys)
        total = querys.count(True)
        logger.debug('send to %s :%s ' % (send_url, total))
        cpus = multiprocessing.cpu_count()
        if cpus > 1:
            pc = cpus - 1
            batch_size = total / pc
        else:
            pc = total / BATCH_SIZE
            batch_size = BATCH_SIZE
        print total, batch_size, pc
        now = datetime.datetime.now()
        for i in range(0, pc):
            skip_query = querys.skip(i * batch_size).limit(batch_size)
            # do_post(skip_query, self.user_dic)
            p = multiprocessing.Process(target=do_post, args=(skip_query, self.user_dic, send_url))
            p.start()
            p.join()
        logger.debug(multiprocessing.active_children())
        logger.debug(multiprocessing.cpu_count())
        write_count_log('\r\n')
        start_content = "Start Time:{0}".format(
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        write_count_log(start_content)
        write_count_log("send to:{0}".format(send_url))
        send_content = "send total urls: {0}".format(total)
        write_count_log(send_content)
        write_count_log("create process:{0}".format(pc))
        self.process_queue()
        write_count_log('total time:{0}'.format(datetime.datetime.now() - now))


    def process_queue(self):
        while not code_queue.empty():
            get_code_data = code_queue.get()
            # if get_data not in self.code_dic.keys():
            self.code_dic[get_code_data] += 1
        write_count_log("code:num")
        for key, value in self.code_dic.items():
            content = '{0}:{1}'.format(key, value)
            write_count_log(content)

        write_count_log("error list:")
        while not fail_queue.empty():
            get_error_data = fail_queue.get()
            write_count_log(get_error_data)


def run(limit, filer_str):
    now = datetime.datetime.now()
    print 'start:', now, limit, filer_str
    logger.debug('run start:%s - %s -  %s' % (now, limit, filer_str))
    rc = Transfer(db.url, limit, filer_str)
    rc.get_urls()
    rc.get_users()
    for url in SEND_URL_LIST:
        rc.send_url(url)
    print 'run end:', datetime.datetime.now() - now
    logger.debug('run end:%s' % (datetime.datetime.now() - now))
    sys.exit()


if __name__ == '__main__':
    filerstr = {}
    limit = LIMIT
    if len(sys.argv) > 2:
        limit = int(sys.argv[1])
        username = sys.argv[2]
        filerstr = {'username': username}
    elif len(sys.argv) > 1:
        limit = int(sys.argv[1])
    else:
        pass

    run(limit, filerstr)
    exit()

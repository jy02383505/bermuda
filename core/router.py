#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2011-5-26

@author: wenwen
"""
from __future__ import with_statement
import simplejson as json
from math import ceil
import sys
import traceback
import logging
from datetime import datetime
import copy
from core import queue, preload_worker_new, database, cert_trans_worker, cert_query_worker, transfer_cert_worker, redisfactory
import dir_refresh
import url_refresh
from util import log_utils
from config import config
from core.generate_id import ObjectId

import physical_refresh
import rpyc
from random import choice
# logger = logging.getLogger('router')
# logger.setLevel(logging.DEBUG)

logger = log_utils.get_router_Logger()

PRELOAD_RATIO = {'preload_task': 1, 'preload_task_h': 2}

CHECK_CACHE = redisfactory.getDB(8)


class Router(object):

    def __init__(self, batch_size=3000, package_size=30):

        self.preload_api_size = 100
        self.batch_size = batch_size
        self.package_size = package_size
        logger.debug('router start. batch_size:%s package_size:%s' %
                     (self.batch_size, self.package_size))
        self.dt = datetime.now()
        self.merged_urls = {}
        self.high_merged_urls ={}
        self.merged_cert = {}
        self.merged_cert_query = {}
        self.merged_transfer_cert = {}
        self.physical_urls = {}

        self.db = database.db_session()
        self.s1_db = database.s1_db_session()

    def run(self):

        # 先执行高优先级队列任务
        logger.debug("refresh_high_router.start")
        #self.refresh_router('url_high_priority_queue')
        self.refresh_high_router()
        logger.debug("refresh_high_router.end")
        # 重置merged_urls
        self.merged_urls = {}
        logger.debug("refresh_router.start")
        self.refresh_router()
        logger.debug("refresh_router.end")

        logger.debug("preload_router.start")
        self.preload_router()
        logger.debug("preload_router.end")

        # logger.debug("preload_report_router.start")
        # self.preload_report_router()
        # logger.debug("preload_report_router.end")

        logger.debug("cert_router.start")
        self.cert_router()
        logger.debug("cert_router.end")

        logger.debug("cert_query_router.start")
        self.cert_query_router()
        logger.debug("cert_query_router.end")

        logger.debug("transfer_cert_router.start")
        self.transfer_cert_router()
        logger.debug("transfer_cert_router.end")

        logger.debug("physical_refresh.start")
        self.physicalrefresh_router()
        logger.debug("physical_refresh.end")

    def cert_router(self, queue_name='cert_task'):
        '''
        证书任务打包
        '''
        try:
            messages = queue.get(queue_name, self.batch_size)
            logger.debug("cert_router %s .work process messages begin, count: %d " %
                         (queue_name, len(messages)))
            for body in messages:
                task = json.loads(body)
                logger.debug('router for cert: %s' % task.get('_id'))
                self.merge_cert(task)
            for tasks in self.merged_cert.values():
                cert_trans_worker.dispatch.delay(tasks)
            logger.info("cert_router %s .work process messages end, count: %d " %
                        (queue_name, len(messages)))
        except Exception:
            logger.warning('cert_router %s work error:%s' % (queue_name, traceback.format_exc()))

    def merge_cert(self, task):

        task['created_time'] = datetime.strptime(task.get("created_time"), "%Y-%m-%d %H:%M:%S")
        send_devs = task['send_devs']
        if send_devs == 'all_hpcc':
            self.merged_cert.setdefault(send_devs, []).append(task)
            if len(self.merged_cert.get(send_devs)) > self.package_size:
                cert_trans_worker.dispatch.delay(self.merged_cert.pop(send_devs))
        else:
            cert_trans_worker.dispatch.delay([task])

    def cert_query_router(self, queue_name='cert_query_task'):
        '''
        证书查询任务
        '''

        try:
            messages = queue.get(queue_name, self.batch_size)
            logger.debug("cert_query_router %s .work process messages begin, count: %d " %
                         (queue_name, len(messages)))
            task_set = {}
            for body in messages:
                task = json.loads(body)
                logger.debug('router for cert_query: %s' % task.get('_id'))
                self.merge_cert_query(task)
            # for k,v in self.merged_cert_query.items():
            for tasks in self.merged_cert_query.values():
                # if len(v) > self.package_size:
                # cert_query_worker.dispatch.delay(self.merged_cert_query.pop(k))
                cert_query_worker.dispatch.delay(tasks)
        except Exception:
            logger.warning('cert_query_router %s work error:%s' %
                           (queue_name, traceback.format_exc()))

    def merge_cert_query(self, task):

        task['created_time'] = datetime.strptime(task.get("created_time"), "%Y-%m-%d %H:%M:%S")
        m = task['dev_ip_md5']
        if self.merged_cert_query.has_key(m):
            self.merged_cert_query[m].append(task)
            if len(self.merged_cert.get(m)) > self.package_size:
                cert_query_worker.dispatch.delay(self.merged_cert.pop(m))
        else:
            self.merged_cert_query[m] = [task]

    def transfer_cert_router(self, queue_name='transfer_cert_task'):
        '''
        证书转移任务
        '''
        try:
            messages = queue.get(queue_name, self.batch_size)
            logger.debug("transfer_cert_router %s .work process messages begin, count: %d " %
                         (queue_name, len(messages)))
            task_set = {}
            for body in messages:
                task = json.loads(body)
                logger.debug('router for transfer_cert: %s' % task.get('_id'))
                self.merge_transfer_cert(task)
            # for k,v in self.merged_cert_query.items():
            for tasks in self.merged_transfer_cert.values():
                # if len(v) > self.package_size:
                # cert_query_worker.dispatch.delay(self.merged_cert_query.pop(k))
                transfer_cert_worker.dispatch.delay(tasks)
        except Exception:
            logger.warning('transfer_cert_router %s work error:%s' %
                           (queue_name, traceback.format_exc()))

    def merge_transfer_cert(self, task):

        task['created_time'] = datetime.strptime(task.get("created_time"), "%Y-%m-%d %H:%M:%S")
        m = task['send_dev_md5']
        if self.merged_transfer_cert.has_key(m):
            self.merged_transfer_cert[m].append(task)
            if len(self.merged_transfer_cert.get(m)) > self.package_size:
                transfer_cert_worker.dispatch.delay(self.merged_transfer_cert.pop(m))
        else:
            self.merged_transfer_cert[m] = [task]

    def refresh_high_router(self, queue_name='url_high_priority_queue'):
        """
        从url_queue中提取url,进行处理

        """
        try:
            messages = queue.get(queue_name, self.batch_size)
            logger.debug("refresh_router %s .work process messages begin, count: %d " %
                         (queue_name, len(messages)))
            for body in messages:
                url = json.loads(body)
                logger.debug('router for url: %s' % url.get('id'))
                if url.get('isdir'):
                    dir_refresh.high_work.delay(url)
                    # todo1 change delay to queue.put
                elif url.get('url_encoding'):
                    url_refresh.high_work.delay([url])
                else:
                    self.high_merge_urlMsg(url)
            for urls in self.high_merged_urls.values():
                url_refresh.high_work.delay(urls)
            logger.info("refresh_router %s .work process messages end, count: %d " %
                        (queue_name, len(messages)))
        except Exception:
            logger.warning('refresh_router %s work error:%s' %
                           (queue_name, traceback.format_exc()))


    def refresh_router(self, queue_name='url_queue'):
        """
        从url_queue中提取url,进行处理

        """
        try:
            messages = queue.get(queue_name, self.batch_size)
            logger.debug("refresh_router %s .work process messages begin, count: %d " %
                         (queue_name, len(messages)))
            for body in messages:
                url = json.loads(body)
                logger.debug('router for url: %s' % url.get('id'))
                if url.get('isdir'):
                    dir_refresh.work.delay(url)
                    # todo1 change delay to queue.put
                elif url.get('url_encoding'):
                    url_refresh.work.delay([url])
                else:
                    self.merge_urlMsg(url)
            for urls in self.merged_urls.values():
                url_refresh.work.delay(urls)
            logger.info("refresh_router %s .work process messages end, count: %d " %
                        (queue_name, len(messages)))
        except Exception:
            logger.warning('refresh_router %s work error:%s' %
                           (queue_name, traceback.format_exc()))

    def preload_router(self):
        """
        处理rabbitmq中preload_task的内容

        """
        try:
            # messages = queue.get('preload_task', self.batch_size)
            messages = self.get_preload_messages()
            if not messages:
                messages = queue.get('preload_task', self.batch_size)

            logger.debug("preload_router.work process messages begin, count: %d " % len(messages))
            url_dict = {}
            url_other = []  # timer, interval, schedule tasks
            url_compressed = []
            for message in messages:
                self.merge_preload_task(message, url_dict, url_other)
            for urls in url_dict.values():
                logger.debug("preload_router url_dict: %s" % url_dict)
                preload_worker_new.dispatch.delay(urls)

            if url_other:
                logger.debug("preload_router url_other: %s" % url_other)
                self.scheduleTask(url_other)

            logger.info("preload_router count: %d" % len(messages))
        except Exception:
            logger.warning('preload_router [error]: %s' % traceback.format_exc())

    def scheduleTask(self, url_list):
        s1_db = database.s1_db_session()

        host_aps = choice(eval(config.get('apscheduler_server', 'host_cluster')))
        logger.debug("scheduleTask host_aps: %s|| url_list: %s" % (host_aps, url_list))
        conn_aps = rpyc.connect(host_aps, int(config.get('apscheduler_server', 'port')), config={
            'allow_public_attrs': True, 'allow_all_attrs': True, 'allow_pickle': True})

        for url in url_list:
            if url.get('task_type') == 'SCHEDULE':
                conn_aps.root.add_job('util.aps_server:preload_worker_new.dispatch.delay', trigger='interval', args=(
                    [url], ), seconds=int(url.get('interval')), start_date=url.get('start_time'), end_date=url.get('end_time'))
            elif url.get('task_type') == 'INTERVAL':
                conn_aps.root.add_job('util.aps_server:preload_worker_new.dispatch.delay', trigger='interval', args=(
                    [url], ), seconds=int(url.get('interval')), end_date=url.get('end_time'))
            elif url.get('task_type') == 'TIMER':
                url['_id'] = ObjectId()
                self.s1_db.preload_url.insert(url)
                rdate = url.get('start_time')
                rdate = rdate if isinstance(rdate, datetime) else datetime.strptime(
                    rdate, '%Y-%m-%d %H:%M:%S')
                run_date_dict = {
                    'year': rdate.year,
                    'month': rdate.month,
                    'day': rdate.day,
                    'hour': rdate.hour,
                    'minute': rdate.minute,
                    'second': rdate.second,
                }
                conn_aps.root.add_job('util.aps_server:preload_worker_new.dispatch.delay',
                                           'cron', args=([url], ), **run_date_dict)
            logger.info("scheduleTask add_job [%s done!] url: %s." %
                        (url.get('task_type'), url.get('url')))

    def get_preload_messages(self):
        try:
            s1_db = database.s1_db_session()

            queue_list = [{i['queue_name']: int(i['queue_ratio'])}
                          for i in self.s1_db.preload_queue_ratio.find({'status': 'ready'})]
            for q in queue_list:
                PRELOAD_RATIO.update(q)
            logger.info('get_preload_messages PRELOAD_RATIO: %s' % (PRELOAD_RATIO, ))
            all_p = sum(PRELOAD_RATIO.values())
            all_m_dict = {}
            for pi, pv in PRELOAD_RATIO.items():
                g_num = int(ceil((pv / float(all_p)) * self.batch_size))
                g_messages = queue.get(pi, g_num)
                # logger.debug('get_preload_messages g_messages key %s  value len %s' %
                #             (pi, len(g_messages)))
                all_m_dict[pi] = g_messages

            sorted_s = sorted(PRELOAD_RATIO.items(), key=lambda x: x[1], reverse=True)
            messages = []
            for k in sorted_s:
                append_key = k[0]
                messages.extend(all_m_dict[k[0]])

            for x in xrange(len(PRELOAD_RATIO)):
                if len(messages) < self.batch_size:
                    left_n = self.batch_size - len(messages)
                    left_m = queue.get(sorted_s[x][0], left_n)
                    messages.extend(left_m)

            logger.info('get_preload_messages messages count %s' % (len(messages)))

            return messages
        except Exception:
            logger.info('get_preload_messages error %s' % (traceback.format_exc()))
            return []

    # original package_size  20
    def merge_preload_task(self, message, url_dict, url_other, package_size=50):
        """
        合并preload任务
        :param message:
        :param url_dict: 实时任务
        :param url_other: 定时任务
        """
        try:
            task = json.loads(message)
            compressed = task.get('compressed')
            task['created_time'] = datetime.strptime(task.get("created_time"), "%Y-%m-%d %H:%M:%S")

            p_key = 'channel_code_%s' % (task.get('channel_code'), )
            productType = CHECK_CACHE.get(p_key)
            if not productType:
                productType = self.db.preload_channel.find_one({'channel_code': task.get('channel_code')}).get('productType')
                CHECK_CACHE.set(p_key, productType)
                CHECK_CACHE.expire(p_key, 60*60)
                logger.debug("merge_preload_task [inIF:productTypeNotExist] productType: %s" % (productType, ))
            logger.debug("merge_preload_task productType: %s" % (productType, ))

            if task.get('status') == 'PROGRESS':  # 实时任务
                url_dict.setdefault(task.get("channel_code"), []).append(task)
                if productType == '1' and compressed:
                    task2 = copy.deepcopy(task)
                    task2['compressed'] = False
                    task2['created_time'] = datetime.strftime(task2['created_time'], "%Y-%m-%d %H:%M:%S")
                    queue.put_json2('preload_task', [task2])
                    logger.debug("merge_preload_task url_dict: %s" % (url_dict, ))

            else:  # timer, interval, schedule tasks
                url_other.append(task)
                if productType == '1' and compressed:
                    task2 = copy.deepcopy(task)
                    task2['compressed'] = False
                    task2['created_time'] = datetime.strftime(task2['created_time'], "%Y-%m-%d %H:%M:%S")
                    queue.put_json2('preload_task', [task2])

            # logger.debug("merge_preload_task url_dict: %s|| url_other: %s" % (url_dict, url_other))
            if len(url_dict.get(task.get("channel_code"), {})) >= package_size:
                preload_worker_new.dispatch.delay(url_dict.pop(task.get("channel_code")))
        except Exception:
            logger.error("merge_preload_task error: %s" % (traceback.format_exc()))

    def physicalrefresh_router(self, queue_name='physical_refresh'):
        """
        从url_queue中提取url,进行处理

        """
        try:
            messages = queue.get(queue_name, self.batch_size)
            logger.debug("refresh_router %s .work process messages begin, count: %d " %
                         (queue_name, len(messages)))
            for body in messages:
                url = json.loads(body)
                logger.debug('router for url: %s' % url.get('id'))
                self.physical_urlMsg(url)
            for urls in self.physical_urls.values():
                physical_refresh.work.delay(urls)
            logger.info("physical refresh_router %s .work process messages end, count: %d " %
                        (queue_name, len(messages)))
        except Exception:
            logger.warning('physical refresh_router: %s|| error: %s' %
                           (queue_name, traceback.format_exc()))

    def high_merge_urlMsg(self, url):
        """
        合并 频道相同的 url
        package_size 默认30条
        :param url:
        """
        # if url.get("url",'').endswith('/'):
        #     url_refresh.work.delay([url])
        # else:
        #     key = url.get('channel_code')
        #     self.merged_urls.setdefault(key,[]).append(url)
        #     if len(self.merged_urls.get(key)) > self.package_size :
        #         url_refresh.work.delay(self.merged_urls.pop(key))
        key = url.get('channel_code')
        self.high_merged_urls.setdefault(key, []).append(url)
        if len(self.high_merged_urls.get(key)) > self.package_size:
            url_refresh.high_work.delay(self.high_merged_urls.pop(key))

    def merge_urlMsg(self, url):
        """
        合并 频道相同的 url
        package_size 默认30条
        :param url:
        """
        # if url.get("url",'').endswith('/'):
        #     url_refresh.work.delay([url])
        # else:
        #     key = url.get('channel_code')
        #     self.merged_urls.setdefault(key,[]).append(url)
        #     if len(self.merged_urls.get(key)) > self.package_size :
        #         url_refresh.work.delay(self.merged_urls.pop(key))
        key = url.get('channel_code')
        self.merged_urls.setdefault(key, []).append(url)
        if len(self.merged_urls.get(key)) > self.package_size:
            url_refresh.work.delay(self.merged_urls.pop(key))

    def physical_urlMsg(self, url):
        """
        合并 频道相同的 url
        package_size 默认30条
        :param url:
        """

        key = url.get('channel_code')
        self.physical_urls.setdefault(key, []).append(url)
        if len(self.physical_urls.get(key)) > self.package_size:
            physical_refresh.work.delay(self.physical_urls.pop(key))

   # def preload_report_router(self):

   #     try:
   #         messages = queue.get('preload_report', self.preload_api_size)
   #         for msg in messages:
   #             preload_worker_new.save_fc_report.delay(msg)
   #     except Exception,e:
   #         logger.warning('preload_report_router work error:%s' % traceback.format_exc(e))


if __name__ == "__main__":
    logger.debug("router begining...")
    router = Router()
    router.run()
    logger.debug("router end.")

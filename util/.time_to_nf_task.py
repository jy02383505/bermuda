"""
1 Check if it is the time first_layer devices are all done.
2 If done, get data from s1_db.preload_nf_task and run worker immediately.
3 If not, wait for done.
"""
from apscheduler.schedulers.background import BackgroundScheduler
from pymongo import MongoClient
from bson import ObjectId
import redis
from sys import exit
import datetime
from core.preload_worker_new import worker
import json
import logging
import os
import time, traceback

M_CONNECT = MongoClient(
    "mongodb://bermuda:bermuda_refresh@223.202.203.31:27017/bermuda_s1")
M = M_CONNECT['bermuda_s1']
R = redis.Redis(host='223.202.203.52', password='bermuda_refresh', port=6379, db=1)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s-%(filename)s[line:%(lineno)d](%(levelname)s): %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='/Application/bermuda/logs/time_to_nf_task.log',
                    filemode='a+')

APS_SCHEDULER_CONFIG = {
    'apscheduler.jobstores.mongo': {
        'type': 'mongodb',
        'client': M,
        'collection': 'apscheduler_temp'
    },
    'apscheduler.executors.default': {
        'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
        'max_workers': '20'
    },
    'apscheduler.executors.processpool': {
        'type': 'processpool',
        'max_workers': '5'
    },
    'apscheduler.job_defaults.coalesce': 'false',
    'apscheduler.job_defaults.max_instances': '20',
    'apscheduler.job_defaults.misfire_grace_time': '30',
    'apscheduler.timezone': 'Asia/Shanghai',
}

def check_sum():
    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(hours=1)
    task_infos = M.preload_nf_task.find({"created_time": {'$gte': start_time, '$lte': end_time}, 'status': 'undone'}).sort('created_time')
    if task_infos.count():
        for task_info in task_infos:
            url = task_info['url']
            firstlayer_dev = task_info['firstlayer_dev']
            layer_dev = task_info['layer_dev']

            content_length = 0
            f_success_count = 0
            delay_times = 0

            for f_dev in firstlayer_dev:
                f_host = f_dev['host']
                dev = R.hget('%s_dev' % str(url['_id']), f_host)
                if not dev:
                    continue
                dev = json.loads(dev)
                if dev['preload_status'] in [200, '200']:
                    f_success_count += 1
                    if content_length == 0:
                        content_length = dev['content_length']

            if content_length:
                wait_sec = get_wait_time(content_length)
                M.preload_nf_task.update_one({'_id': task_info['_id']}, {'$set': {'wait_sec': wait_sec}})

            if f_success_count == len(firstlayer_dev):
                M.preload_nf_task.update_one({'_id': task_info['_id']}, {'$set': {'status': 'done'}})

def preload_nf():
    task_infos = M.preload_nf_task.find({'status': 'done'}).sort('created_time')
    url_list = []
    if task_infos.count():
        for task_info in task_infos:
            url = task_info['url']
            firstlayer_dev = task_info['firstlayer_dev']
            layer_dev = task_info['layer_dev']

            ### nf tasks begin
            worker([url], layer_dev, True)
            M.preload_nf_task.remove({'_id': task_info['_id']})
            url_list.append(str(url['_id']))
    logging.info('preload_nf finished(deleted) -> url_list: %s' % url_list)


def get_wait_time(content_length):
    content_length = float(content_length)
    wait_sec = 5 if content_length < 15 * 1024 * 1024 else content_length / (3 * 1024 * 1024)
    return wait_sec


if __name__ == '__main__':
    now = datetime.datetime.now()
    print '\n-----now-----\n', now
    # after_sec = now + datetime.timedelta(seconds=5)

    scheduler = BackgroundScheduler(APS_SCHEDULER_CONFIG)
    # scheduler.add_job(check_sum, 'date', run_date=after_sec)

    scheduler.add_job(check_sum, 'interval', seconds=15)
    scheduler.add_job(preload_nf, 'interval', seconds=20)

    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        while True:
            time.sleep(2)
    except Exception, e:
        logging.debug('Run apscheduler tasks error: %s' % traceback.format_exc(e))
        scheduler.shutdown()


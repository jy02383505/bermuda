#!/usr/bin/env python
# coding: utf-8

import traceback
import time
from datetime import datetime, timedelta


def get_time():
    return time.strftime('%Y-%m-%d %H:%M:%S') + '.%s' % datetime.now().microsecond


"""
This is an example showing how to make the scheduler into a remotely accessible service.
It uses RPyC to set up a service through which the scheduler can be made to add, modify and remove
jobs.
To run, first install RPyC using pip. Then change the working directory to the ``rpc`` directory
and run it with ``python -m aps_server``.
"""

import rpyc
import os

from rpyc.utils.server import ThreadedServer
from apscheduler.schedulers.background import BackgroundScheduler

from core import preload_worker_new
from util import log_utils
from core.config import config

logger = log_utils.get_preload_Logger()


APSCHEDULER_CONFIG = {
    'apscheduler.jobstores.default': {
        'type': 'redis',
        'host': config.get('redis', 'host'),
        'port': 6379,
        'db': 8,
        'password': config.get('redis', 'password')
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


def print_text(text):
    print('print_text text: %s' % (text, ))
    logger.info('print_text text: %s' % (text, ))

# def dispatchIt(urls):
#     logger.info('dispatchIt urls: %s' % (urls, ))
#     preload_worker_new.dispatch.delay(urls)
#     logger.info('dispatchIt Done.')


class SchedulerService(rpyc.Service):

    def exposed_add_job(self, func, *args, **kwargs):
        return scheduler.add_job(func, *args, **kwargs)

    def exposed_modify_job(self, job_id, jobstore=None, **changes):
        return scheduler.modify_job(job_id, jobstore, **changes)

    def exposed_reschedule_job(self, job_id, jobstore=None, trigger=None, **trigger_args):
        return scheduler.reschedule_job(job_id, jobstore, trigger, **trigger_args)

    def exposed_pause_job(self, job_id, jobstore=None):
        return scheduler.pause_job(job_id, jobstore)

    def exposed_resume_job(self, job_id, jobstore=None):
        return scheduler.resume_job(job_id, jobstore)

    def exposed_remove_job(self, job_id, jobstore=None):
        scheduler.remove_job(job_id, jobstore)

    def exposed_get_job(self, job_id):
        return scheduler.get_job(job_id)

    def exposed_get_jobs(self, jobstore=None):
        return scheduler.get_jobs(jobstore)

scheduler = BackgroundScheduler(APSCHEDULER_CONFIG)

def run():
    logger.info('\n---(%s)beforeStart.---\n%s' % (get_time(), 'beforeStart.', ))
    scheduler.start()
    logger.info('\n---(%s)"schedulerStarted."---\n%s' % (get_time(), "schedulerStarted.", ))
    protocol_config = {'allow_public_attrs': True, 'allow_all_attrs': True, 'allow_pickle': True}
    server = ThreadedServer(SchedulerService, port=int(config.get('apscheduler_server', 'port')), protocol_config=protocol_config)
    try:
        logger.info('\n---(%s)"beforeServerStart."---\n%s' % (get_time(), "beforeServerStart.", ))
        server.start()
        logger.info('\n---(%s)"serverStarted."---\n%s' % (get_time(), "serverStarted.", ))
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        scheduler.shutdown()

#! -*- coding=utf-8 -*-
import simplejson as json
import logging
from cache.rediscache import DEV_NUMBER_NAME,DEV_CHANNEL_LIKED_FIRST,DEV_CHANNEL_CACHE,DEV_CHANNEL_LIKED
from cache.rediscache import firstlayer_cache,device_cache,DEVICES_PREFIX,FIRSTLAYER_DEVICES_PREFIX
from core.config import config
import traceback
import pika
import simplejson as sjson
from core.database import query_db_session, db_session, s1_db_session
import datetime
from core.fail_task_refresh import send_device_open
# LOG_FILENAME = '/Application/bermuda/logs/update_redis_channel_customer.log'
# logging.basicConfig(filename=LOG_FILENAME,
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(process)d - Line:%(lineno)d - %(message)s',
#                     level=logging.INFO)
#
# logger = logging.getLogger('update_redis_channel_customer')
# logger.setLevel(logging.DEBUG)

LOG_FILENAME = '/Application/bermuda/logs/update_cms_device_status.log'
# LOG_FILENAME = '/home/rubin/logs/update_redis_channel_customer.log'
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(process)d - Line:%(lineno)d - %(message)s")
fh = logging.FileHandler(LOG_FILENAME)
fh.setFormatter(formatter)

logger = logging.getLogger('update_cms_device_status')
logger.addHandler(fh)
logger.setLevel(logging.DEBUG)


def load_task(body):
    """
    parse json data
    :param body:
    :return:
    """
    try:
        return json.loads(body)
    except Exception, e:
        logger.debug("parse json data:%s, error:%s" % (body, e))
        return {'oldSerialNumber': 0, 'status': []}


def get_device_name(dev_number):
    dev_name = DEV_CHANNEL_CACHE.hget(DEV_NUMBER_NAME,dev_number)
    return dev_name


def get_device_channel(dev_name):
    channel_list = DEV_CHANNEL_CACHE.smembers(DEV_CHANNEL_LIKED % dev_name)
    channel_first_list = DEV_CHANNEL_CACHE.smembers(DEV_CHANNEL_LIKED_FIRST % dev_name)
    return channel_list,channel_first_list


def change_device_status(channel_code,dev_name,dev_status,upper=False):
    # DEVICES_PREFIX='d_by_%s'
    # FIRSTLAYER_DEVICES_PREFIX='fd_by_%s'
    if upper :
        red = firstlayer_cache
        redis_key = FIRSTLAYER_DEVICES_PREFIX % channel_code
    else:
        red = device_cache
        redis_key = DEVICES_PREFIX % channel_code
    try:
        hh = red.hget(redis_key,dev_name)
        new_dict = json.loads(hh)
        print new_dict
        new_dict.update({"status": dev_status})
        data = sjson.JSONEncoder().encode(new_dict)
        red.hset(redis_key,dev_name,data)
    except Exception,e:
        logger.debug("change device status error :%s" % (e))
        logger.info("change device status error channel_code:{0},dev_name :{1}".format(channel_code,dev_name))


def on_message(channel, method_frame, header_frame, body):
    # channel.queue_declare(queue=body, auto_delete=True)
    print "body:%s" % body
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)

    logger.info("refresh device body:{0}".format(body))

    result = {}
    try:
        # {"ROOT": {"HEADER": {}, "BODY": {"BUSI_INFO": {"oldSerialNumber": "1000103331", "status": "OPEN"}}}}
        result = load_task(body).get('ROOT').get('BODY').get('BUSI_INFO')
    except Exception, e:
        logger.error("result error:%s" % traceback.format_exc(e))
        logger.info('result frame.body:%s' % body)
    try:
        dev_number = result.get("oldSerialNumber")
        dev_status = result.get("status")

        if dev_number and dev_status:
            logger.info("refresh dev_number:{0},status:{1}".format(dev_number,dev_status))
            dev_name = get_device_name(dev_number)

            channel_list,first_channel_list = get_device_channel(dev_name)
            for channel_code in channel_list:
                change_device_status(channel_code,dev_name,dev_status)
            for channel_code in first_channel_list:
                change_device_status(channel_code,dev_name,dev_status,upper=True)
            # if dev_status not in ["OPEN"]:
            db_s1 = s1_db_session()
            db_s1.device_status_change.insert({"hostname": dev_name, "status": dev_status, "datetime": datetime.datetime.now()})
            if dev_status in ["OPEN"]:
                send_device_open.delay(dev_name)

    except Exception,e:
        logger.info("refreshed dev failed")
        pass


def main_fun():
    """
    main of the function
    :return:
    """
    credentials = pika.PlainCredentials(config.get('rcms_activemq', 'username'), config.get('rcms_activemq', 'password'))
    # parameters =  pika.ConnectionParameters('223.202.203.52', credentials=credentials, virtual_host='cms3')
    parameters =  pika.ConnectionParameters(config.get('rcms_activemq', 'host'),port=5672, credentials=credentials, virtual_host='cms3')
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()
    # channel.exchange_declare(exchange="test_exchange", exchange_type="direct", passive=False, durable=True, auto_delete=False)
    channel.queue_declare(queue="CMS3.device.refresh", durable=True, auto_delete=False)
    # channel.queue_bind(queue="rabbit.test", exchange="test_exchange", routing_key="standard_key")
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(on_message, 'CMS3.device.refresh')
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()

if __name__ == '__main__':
    main_fun()

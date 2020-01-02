#coding=utf-8
import threading
from time import ctime,sleep
from core import database
from cache.api_mongo import ApiMongo
from core import  redisfactory
import datetime
# 链接mongo 句柄
db = database.query_db_session()
portal_redis = redisfactory.getDB(13)
USERNAME_LIST_KEY = "usernames"
CHANNEL_LIST_KEY = 'activechannels'
CHANNEL_LIST_EX = "ExpireChannel"
CHANNEL_REFRESH_TIME = 5 #刷新频道的时间

ThreadNum = 20


def get_api():
    api = ApiMongo()
    return api


def get_channel():
    create_time = portal_redis.get(CHANNEL_LIST_EX)
    channel_set = portal_redis.smembers(CHANNEL_LIST_KEY)
    if not create_time or not channel_set:
        now = datetime.datetime.now().strftime("%Y%m%d%H")
        portal_redis.set(CHANNEL_LIST_EX,now)

        channel_set = db.url.distinct("channel_code")
        for channel in channel_set:
            portal_redis.sadd(CHANNEL_LIST_KEY, channel)
        return channel_set
    else:
        new_time = datetime.datetime.strptime(create_time, "%Y%m%d%H")+datetime.timedelta(days=CHANNEL_REFRESH_TIME)
        now = datetime.datetime.now()
        if new_time < now:
            now = datetime.datetime.now().strftime("%Y%m%d%H")
            portal_redis.set(CHANNEL_LIST_EX, now)
            portal_redis.delete(CHANNEL_LIST_KEY)
            channel_set = db.url.distinct("channel_code")
            for channel in channel_set:
                portal_redis.sadd(CHANNEL_LIST_KEY, channel)
            return channel_set
        else:
            return channel_set

def get_username():
    create_time = portal_redis.get(CHANNEL_LIST_EX)
    if not create_time:
        now = datetime.datetime.now().strftime("%Y%m%d%H")
        portal_redis.set(CHANNEL_LIST_EX, now)
    new_time = datetime.datetime.strptime(create_time, "%Y%m%d%H") + datetime.timedelta(days=CHANNEL_REFRESH_TIME)
    now = datetime.datetime.now()
    username_set = portal_redis.smembers(USERNAME_LIST_KEY)
    if new_time < now or not username_set :
        username_set = []
        sts = db.statistical.find({}, {'username_list': 1}).sort("date", -1).limit(CHANNEL_REFRESH_TIME)
        for usr_names in sts:
            username_set = username_set + usr_names.get('username_list')
        pipe = portal_redis.pipeline()
        pipe.delete(USERNAME_LIST_KEY)
        for username in username_set:
            pipe.sadd(USERNAME_LIST_KEY, username)
        pipe.execute()
        return set(username_set)
    else:
        return username_set


def syn_redis(api, channel_code):
    api.sync_devices(channel_code)
    api.sync_firstLayer_devices(channel_code)

def syn_user_channel(api,username):
    api.sync_channels(username)

def syn_chanel_status():
    api = get_api()
    username_set = get_username()
    us_length = len(username_set)
    us_pack = us_length/ThreadNum + 1
    for i in range(us_pack):
        users = username_set[i*ThreadNum:(i+1)*ThreadNum]
        threads = []
        for user in users:
            t1 = threading.Thread(target=syn_user_channel, args=(api, user))
            threads.append(t1)
        for t2 in threads:
            t2.start()
        for t3 in threads:
            t3.join()

def chanel_devices():
    api = get_api()
    channel_set = get_channel()
    ch_length = len(channel_set)
    channel_pack = ch_length/ThreadNum + 1
    for i in range(channel_pack):
        code_set = channel_set[i*ThreadNum:(i+1)*ThreadNum]
        threads = []
        for code in code_set:
            t1 = threading.Thread(target=syn_redis, args=(api, code))
            threads.append(t1)
        for t2 in threads:
            t2.start()
        for t3 in threads:
            t3.join()

def run():
    syn_chanel_status()
    chanel_devices()
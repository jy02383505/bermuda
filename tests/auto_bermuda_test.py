# -*- coding:utf-8 -*-
'''
Created on 2011-6-7

@author: wenwen
'''
import urllib
from random import Random
from multiprocessing import Process
import httplib
import datetime
from core.database import query_db_session
import time
from bson import ObjectId
import logging
import sys,os


LOG_FILENAME = '/Application/bermuda/logs/auto_bermuda_test.log'
logging.basicConfig(filename=LOG_FILENAME, format='%(asctime)s - %(name)s - %(levelname)s - %(process)d - Line:%(lineno)d - %(message)s', level=logging.DEBUG)

logger = logging.getLogger('bermuda')
logger.setLevel(logging.DEBUG)

def random_str(randomlength = 8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str

def do_post(params,serverIp):
    f = urllib.urlopen("http://"+serverIp+"/content/refresh" , params)
    content =  f.read()
    exec('request=%s' %content)
    print content
    getStatus(request.get('r_id'))
    #getStatus('50bc1dbf414ec05c34468bcf')

def getStatus(r_id):
    print "url check begining .......... %s " % os.getpid() 
    begin = datetime.datetime.now()
    while True:
        firstLayer = []
        notfirstLayer = []
        devices = []
        finishCount = 0
        processCount = 0
        time.sleep(30)
        db = query_db_session()
        request = db.request.find_one({"_id":ObjectId(r_id)})
        refresh_msg  = "\n ********************************************** %s " % os.getpid() 
        refresh_msg += "\n\t-------------------------------------------  "
        refresh_msg += "\n\t request status : %s"  % str(request.get('status'))
        urlList  = [ url  for url in db.url.find({"r_id":ObjectId(r_id)})]
        for url in urlList:
            refresh_msg += u"\n\t url : %s , status: %s " %( str(url.get("url","no url").encode('utf-8')) , str(url.get("status","NO STATUS")))
            successCount = 0
            if url != None and url.get('dev_id','') != '' :
                device = db.device.find_one({"_id":url.get('dev_id')})
                refresh_msg += "\n\t\t device_id: %s " % (url.get('dev_id'))
                firstLayer = []
                notfirstLayer = []
                devices = device['devices']
                for key in devices.keys():
                    if devices.get(key).get('code') >0 :
                        successCount = successCount +1
                    if devices.get(key).get('firstLayer') == True:
                        firstLayer.append(devices.get(key))
                    else:
                        notfirstLayer.append(devices.get(key))
            else:
                refresh_msg += "\n\t\t no device_id "
            refresh_msg += "\n\t\t total devices: %d ,success device : %d , firstLayer: %d ,notfirstLayer: %d " %(len(devices),successCount,len(firstLayer), len(notfirstLayer))   
            if len(firstLayer)>0:
                tiered = u" firstLayer"
            else :
                tiered = u" notfirstLayer"
            if url.get('status') == "FINISHED":
                refresh_msg += u"\n\t\t url refresh FINISHED , %s " % tiered
                finishCount = finishCount +1
            else :
                if successCount>0:
                    processCount = processCount+1
                refresh_msg += u"\n\t\t url refresh  PROGRESS, %s " % tiered
            refresh_msg +="\n\t-------------------------------------------  "
        end = datetime.datetime.now()
        refresh_msg +="\n\t result : count: %d , finish count : %d , processing count : %d , not start : %d" %(len(urlList),finishCount,processCount,(len(urlList)-finishCount-processCount))        
        refresh_msg += "\n ************************************ times :%d " % (end-begin).seconds
        print refresh_msg
        logger.debug(refresh_msg) 
        if len(urlList) == finishCount or (end-begin).seconds > 500 :
            break
    print "url check ending ............ %s " % os.getpid() 


def do_3post():
    for i in range(0, 1):
        #params =  urllib.urlencode({'userID': 'chinacache','user': 'chinacache', 'pswd': '!QAZ2wsx', 'urls': '0005$http://www.chinacache.com/uv1rCKmmCOOLER.jpg@_@','ok':'ok'})
        params =  urllib.urlencode({'userID': 'marykay','user': 'marykay', 'pswd': 'Marykay!@34', 'urls': '0005$http://www.marykay.com.cn/test/sCan.jpg@_@','ok':'ok'})
        response =urllib.urlopen("http://223.202.40.159/indexPortal.jsp" , params)
        print response.read()

if __name__ == '__main__':
    #print sys.argv
    #params = urllib.urlencode({'username': 'sina_t', 'password': 'MTE3YjU2ZTlhNmNl', 'task': '{"urls":["http://ww1.sinaimg.cn/bmiddle/test/cooler.jpg"]}'})
    #dirParams = urllib.urlencode({'username': 'geili', 'password': '!WPR)ymL', 'task': '{"dirs":["http://imgcc01.geilicdn.com/taobao21422880516*"],"callback":{"email":["peng.zhou@chinacache.com","418435432@qq.com"],"acptNotice":true}}'})
    #params = urllib.urlencode({'username': 'snda', 'password': 'ptyy@snda.com', 'task': '{"urls":["http://dl.autopatch.ccgslb.net/test/a.jpg","http://dl.autopatch.ccgslb.net/test/b.jpg"]}'})
    
    params = urllib.urlencode({'username': 'duowan', 'password': '5VGO3LB62O', 'task': '{"urls":["http://web.duowan.com/51seer/jingling/img/1361.jpg"]}'})
    Process(target = do_post,args=(params,"127.0.0.1",)).start()
    params = urllib.urlencode({'username': 'duowan', 'password': '5VGO3LB62O', 'task': '{"urls":["http://web.duowan.com/51seer/jingling/img/cooler1.jpg","http://web.duowan.com/51seer/jingling/img/cooler2.jpg"]}'})
    Process(target = do_post,args=(params,"127.0.0.1",)).start()

    params = urllib.urlencode({'username': 'duowan', 'password': '5VGO3LB62O', 'task': '{"urls":["http://web.duowan.com/51seer/jingling/img/1361.jpg","http://web.duowan.com/51seer/jingling/img/1361.jpg"]}'})
    Process(target = do_post,args=(params,"127.0.0.1",)).start()

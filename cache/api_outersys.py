# -*- coding:utf-8 -*-
__author__ = 'root'
import urllib2,traceback,string
import simplejson as sjson
import json

from util import log_utils

logger = log_utils.get_redis_Logger()


RETRY_TIMES=4
TIMEOUT_OUTERURL=60
class ApiOuter(object):
    def read_from_outer(self,url,times=1,need_retry=True, time_out=0):
        try:
            '''backspace is existed'''
            # raise urllib2.HTTPError
            # raise urllib2.HTTPError("", 670, "", None, None)
            # raise UnicodeError
            url = string.replace(url,' ','%20')
            if time_out == 0:
                out_objects = urllib2.urlopen(url,timeout=TIMEOUT_OUTERURL).read()
            else:
                logger.warn('ApiOuter  read_from_outer time_out:%s, url:%s' % (time_out, url))
                out_objects = urllib2.urlopen(url, timeout=time_out).read()


            if out_objects:
                return out_objects
            else:
                raise 'object is null from url %s' % url

        except UnicodeError, e:
            logger.error('ApiOuter UnicodeError error, url:%s, error:%s, times:%s' % (url, traceback.format_exc(e), times))
            url=url.encode('utf-8')
            return self.retry(url, times)
        except urllib2.HTTPError, e:
            logger.error('ApiOuter HTTPError error, url:%s, error:%s, times:%s' % (url, traceback.format_exc(e), times))
            # if (string.count(url, '/')>1):
            #     return None
            # logger.error('for url== [%s] for times %d read_from_outer  exception is : %s' % (url,times,traceback.format_exc(e)))
            # url=urllib2.quote(url)
            return self.retry(url,times)
        except Exception, e:
            logger.error('for url== [%s] for times %d read_from_outer  exception is : %s' % (url,times,traceback.format_exc(e)))
            if (need_retry) :
                return self.retry(url,times)
            else:
                return None

    def read_post_cms_outer(self,url,channlcode,times=2,need_retry=True, time_out=0):
        devList = []
        try:

            values = {
                "ROOT": {
                    "HEADER": {
                        "AUTH_INFO": {
                            "LOGIN_NO": "refresh_preload@chinacache.com",
                            "LOGIN_PWD": "cert_2018_Q1",
                            # "FUNC_CODE": "9072"
                        }
                    },
                    "BODY": {
                        "BUSI_INFO": {
                            "extnIds": ['{}'.format(channlcode)]
                        }
                    }
                }
            }
            send_headers = {
                'Content-Type': 'application/json'
            }
            jdata = json.dumps(values)
            status = ''
            for i in range(times):
                try:
                    request = urllib2.Request(url, jdata, headers=send_headers)
                    request = urllib2.urlopen(request)
                    result = json.loads(request.read())
                    # print result
                    logger.debug("gray channlcode:{},data:{}".format(channlcode,result))
                    if result['ROOT']['BODY']['RETURN_MSG'] == 'OK':
                        status = 'OK'
                        print 'OK'

                        devList = result['ROOT']['BODY']['OUT_DATA']['GRAY_DEV_INFO']
                        return  devList
                        # check_result = json.loads(request.read())
                        # print check_result
                except Exception, e:
                    print e

        except Exception, e:
            logger.debug(traceback.format_exc())
        return devList

    def retry(self,url,times):
        times+=1
        if (times>RETRY_TIMES):
            return None
        else:
            return self.read_from_outer(url,times)

    def get_valid_jsonstr(self,jsonStr):
        try:
            return sjson.loads(jsonStr)
        except Exception, e:
            logger.error("Passed, The string: %s  is not a valid json string, pass it" % jsonStr)
            return False

    def utfize_username(self,user_name):
        user_name_utf8=user_name
        try:
            user_name_utf8=user_name.encode('utf-8')
        except UnicodeEncodeError,e:
            logger.debug('user name is not utf8,username== %s' % user_name)
            user_name_utf8=user_name
        # logger.warn('sync_allObjects.utfize_username---user_name==%s ' % user_name_utf8)
        return user_name_utf8
    def is_diff_sort_cmp(self,devices_rcms,devices_mongo):
        if devices_rcms!=devices_mongo:
            return True
        else:
            return False
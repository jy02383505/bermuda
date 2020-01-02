#! -*- coding=utf-8 -*-
"""
@version: ??
@author: rubin
@license:
@contact: longjun.zhao@chinacache.com
@site: 
@software: PyCharm
@file: test_chinaese.py
@time: 17-5-25 上午10:15
"""
import sys
import uuid
from xml.dom.minidom import parseString
import logging

# LOG_FILENAME = '/Application/bermuda/logs/bermuda_tools.log'
LOG_FILENAME = '/home/rubin/logs/bermuda_tools.log'
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(process)d - Line:%(lineno)d - %(message)s")
fh = logging.FileHandler(LOG_FILENAME)
fh.setFormatter(formatter)

logger = logging.getLogger('monitor_region_devs')
logger.addHandler(fh)
logger.setLevel(logging.DEBUG)
# reload(sys)
print sys.getdefaultencoding()


a = '你好'
b = u'你好'
print(type(a), len(a))
print(type(b), len(b))


str1 = "123你好"
str4 = unicode(str1, 'utf8')
str2 = str1.decode('utf8')
str3 = str2.encode('gb2312')
print str3
print type(str2)


def is_chinese(uchar):
    """
    judge a unicode is chinese or not
    Args:
        uchar:

    Returns:

    """
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False


sys.getdefaultencoding()
print  "sasdf", sys.getdefaultencoding()
# str2 = u'你好'
for uchar in str4:
    print 'uchar:%s' % uchar
    if is_chinese(uchar):
        print "k1"
    else:
        print 'k2'


def getUrlCommand(urls):
    """
    按接口格式，格式化url
    :param urls:
    :return:
    """
    sid = uuid.uuid1().hex
    content = parseString('<method name="url_expire" sessionid="%s"><recursion>0</recursion></method>' % sid)
    if urls[0].get('action') == 'purge':
        content = parseString('<method name="url_purge" sessionid="%s"><recursion>0</recursion></method>' % sid)
    url_list = parseString('<url_list></url_list>')
    tmp = {}
    logger.debug('urls information')
    logger.debug(urls)
    for idx, url in enumerate(urls):
        if url.get("url") in tmp:
            continue
        qurl = url.get("url").lower() if url.get('ignore_case', False) else url.get("url")
        uelement = content.createElement('url')
        #uelement.setAttribute('id', str(idx))
        uelement.setAttribute('id', url.get("id", str(idx))) #store url.id  in id
        logger.debug("send url.id:%s" % url.get("id"))
        # rubin test start
        # qurl = qurl.decode('utf8')
        # qurl = qurl.encode('gb2312')
        # rubin test end
        uelement.appendChild(content.createTextNode(qurl))
        url_list.documentElement.appendChild(uelement)
        tmp[url.get("url")] = ''
    content.documentElement.appendChild(url_list.documentElement)
    return content.toxml('utf-8')
    # return content.toxml('gbk')
    # return content.toxml('gb2312')
    # return content.toxml('gb18030')
    # return content.toxml('big5')


if __name__ == "__main__":
    urls = [{'url': "asdfhttp://www.baidu.com/1", 'ignore_case': True, 'id': "1234sdfsdf"}]
    print getUrlCommand(urls)
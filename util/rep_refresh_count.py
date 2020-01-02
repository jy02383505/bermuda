#-*- coding:utf-8 -*-
import pymongo
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import timeout_decorator
from util.emailSender import EmailSender
from collections import Counter
from core import database

Host = '223.202.203.88'
def get_host(host,db_name):
    client = pymongo.MongoClient(host=host, port=27017)
    db = client[db_name]
    db.authenticate('bermuda', 'bermuda_refresh')
    return db
def get_HPCC_num(act_time,end_time):
    all_num = 0
    all_err_num = 0
    # host = "223.202.203.93"
    # db_name = 'bermuda'
    # db_ber = get_host(host, db_name)
    db_ber = database.db_session()
    connect_day = db_ber['devices_status_day']

    device_one = connect_day.find_one({'date': {'$gte': act_time, '$lt': end_time}})
    dev_dict = device_one.get("HPCC")
    return dev_dict.get('200',1)
def get_all_num(act_time,end_time):
    all_num = 0
    all_err_num = 0
    # host = Host
    # db_name = 'bermuda_s1'
    # db = get_host(host,db_name)
    db = database.s1_db_session()
    for i in range(10):
        try:
            print ('-------------{0}--------'.format(i))
            sql_q = "refresh_result{}".format(i)
            #db_num = db[sql_q].find({"result":"200",'time': {'$gt': act_time, '$lt': end_time}}).count()
            #err_num = db[sql_q].find({"result": {"$ne":"200"}, 'time': {'$gt': act_time, '$lt': end_time}}).count()
            db_num = 0
            while True:
                try:
                    db_num,err_num = get_all_err_num(db, sql_q, act_time, end_time)
                    break
                except Exception as e:
                    print ("超时:{}".format(i))
                    pass

            all_num += db_num
            all_err_num += err_num
        except Exception as e:
            pass
    return all_num,all_err_num
@timeout_decorator.timeout(300)
def get_all_err_num(sql_db,sql_str,act_time,end_time):
    # db_num = sql_db[sql_str].find({"result": "200", 'time': {'$gt': act_time, '$lt': end_time}}).count()
    # err_num = sql_db[sql_str].find({"result": {"$ne": "200"}, 'time': {'$gt': act_time, '$lt': end_time}}).count()
    db_num = sql_db[sql_str].find({"result": {"$in": ["200","404"]}, 'time': {'$gt': act_time, '$lt': end_time}}).count()
    err_num = sql_db[sql_str].find({"result": {"$nin": ["200", "404"]}, 'time': {'$gt': act_time, '$lt': end_time}}).count()
    return  db_num,err_num

# 发邮件
def send_email(to_addrs, subject, content):
    msg = MIMEMultipart()
    from_addr = 'nocalert@chinacache.com'
    msg['Subject'] = subject
    msg['From'] = from_addr
    msgText = MIMEText(content, 'html', 'utf-8')
    msg.attach(msgText)
    if type(to_addrs) == str:
        msg['To'] = to_addrs
    elif type(to_addrs) == list:
        msg['To'] = ','.join(to_addrs)

    e_s = EmailSender(from_addr, to_addrs, msg)
    r_send = e_s.sendIt()
    if r_send != {}:
        s = smtplib.SMTP('anonymousrelay.chinacache.com')
        try:
            s.ehlo()
            s.starttls()
            s.ehlo()
        except Exception as ex:
            pass
        s.sendmail(from_addr, to_addrs, msg.as_string())
        s.quit()
def get_refresh_num():
    now_1 = datetime.datetime.now()
    print (now_1)
    now = datetime.date.today()

    now_day = now - datetime.timedelta(days=0)
    now_day_2 = now - datetime.timedelta(days=1)
    now_day = datetime.datetime.combine(now_day, datetime.datetime.min.time())
    now_day_2 = datetime.datetime.combine(now_day_2, datetime.datetime.min.time())
    print (now_day_2, now_day)
    # print (dddddd(now_day_2,now_day))
    success_num, fail_num = get_all_num(now_day_2, now_day)
    All_Num = get_HPCC_num(now_day_2, now_day)
    now2 = datetime.datetime.now()
    print (now2)

    #content = "日期：{0}\r\n总数量：{1},回调成功个数：{2},回调失败个数：{3},回调百分比{4}".format(now_day_2, All_Num, success_num, fail_num,
    #                                                                   (success_num + fail_num) / 1.0 / All_Num)
    # content = 'hello'
    #to_addrs = ['pengfei.hao@chinacache.com', 'huan.ma@chinacache.com']
    #subject = '统计刷新成功回调数量'
    #send_email(to_addrs, subject, content)
    my_table = write_statistical(All_Num,success_num,fail_num)
    return my_table

def write_statistical(All_Num,success_num,fail_num):

    today = datetime.datetime.today()
    process_date = today - datetime.timedelta(days=1)
    date_str = process_date.strftime('%Y-%m-%d')

    header_list = ['Date', 'HPCC下发成功数量', '回调成功数量', '回调失败数量','未返回数量' ,'回调成功百分比']

    theader = '<th>{0}</th>'.format('</th><th>'.join(header_list))
    trs = []
    tr = [date_str]
    tr.append('{0:,}'.format(All_Num))
    tr.append('{0:,}'.format(success_num))
    tr.append('{0:,}'.format(fail_num))
    tr.append('{0:,}'.format(All_Num-fail_num-success_num))
    tr.append('{0:.2%}'.format((round(success_num/ float(All_Num), 4))))

    trs.append('<td>{0}</td>'.format('</td><td>'.join(tr)))
    table = '<table border="1">\n<thead><tr>{0}</tr></thead>\n<tbody>\n<tr>{1}</tr></tbody></table>'.format(theader,'</tr>\n<tr>'.join(trs))
    return table



def get_fail_dev_num():
    now_1 = datetime.datetime.now()
    print (now_1)
    now = datetime.date.today()

    now_day = now - datetime.timedelta(days=0)
    now_day_2 = now - datetime.timedelta(days=1)
    now_day = datetime.datetime.combine(now_day, datetime.datetime.min.time())
    now_day_2 = datetime.datetime.combine(now_day_2, datetime.datetime.min.time())
    print (now_day_2, now_day)
    # print (dddddd(now_day_2,now_day))
    my_table = get_fail_device_num(now_day_2, now_day)
    return my_table
def get_fail_device_num(act_time,end_time):
    all_num = 0
    all_err_num = 0
    host = Host
    devices_list_all = []
    # db_name = 'bermuda_s1'
    # db = get_host(host,db_name)
    db = database.s1_db_session()
    for i in range(10):
        try:
            print ('-------------{0}--------'.format(i))
            sql_q = "refresh_result{}".format(i)
            while True:
                try:
                    devices_list = get_all_err_device(db, sql_q, act_time, end_time)
                    print devices_list
                    break
                except Exception as e:
                    print ("超时:{}".format(i))
                    pass

            devices_list_all = devices_list_all + devices_list
        except Exception as e:
            pass
    pai_dev = Counter(devices_list_all).most_common(10)
    my_dev_table = write_statistical_dev(pai_dev)
    return my_dev_table
@timeout_decorator.timeout(300)
def get_all_err_device(sql_db,sql_str,act_time,end_time):
    fail_devices = sql_db[sql_str].find({"result": {"$nin": ["200", "404"]}, 'time': {'$gt': act_time, '$lt': end_time}})
    devices_list = [fail.get("hostname",'unkown') for fail in fail_devices]
    return devices_list

def write_statistical_dev(devices_list_all):

    header_list = ['NO.', '设备名称', '数量']

    theader = '<th>{0}</th>'.format('</th><th>'.join(header_list))

    table = ""
    i = 0
    trs = []
    for data in devices_list_all:
        key = data[0]
        value = data[1]
        tr = [str(i + 1)]
        tr.append(key)
        tr.append('{0:,}'.format(int(value)))
        trs.append('<td>{0}</td>'.format('</td><td>'.join(tr)))
        i += 1
    table += '<table width="33%" border="1" >\n<thead><tr>{0}</tr></thead>\n<tbody>\n<tr>{1}</tr></tbody></table>'.format(
        theader,
        '</tr>\n<tr>'.join(
            trs))
    return table
if __name__ == "__main__":
    now_1 = datetime.datetime.now()
    print (now_1)
    now  = datetime.date.today()

    now_day = now -datetime.timedelta(days=0)
    now_day_2 = now - datetime.timedelta(days=1)
    now_day = datetime.datetime.combine(now_day, datetime.datetime.min.time())
    now_day_2 = datetime.datetime.combine(now_day_2, datetime.datetime.min.time())
    print (now_day_2,now_day)
    #print (dddddd(now_day_2,now_day))
    success_num,fail_num =get_all_num(now_day_2,now_day)
    All_Num = get_HPCC_num(now_day_2,now_day)
    now2 = datetime.datetime.now()
    print (now2)

    content = "日期：{0}\r\n总数量：{1},回调成功个数：{2},回调失败个数：{3},回调百分比{4}".format(now_day_2,All_Num,success_num,fail_num,(success_num+fail_num)/1.0/All_Num)
    #content = 'hello'
    to_addrs = ['pengfei.hao@chinacache.com','huan.ma@chinacache.com']
    subject = '统计刷新成功回调数量'
    send_email(to_addrs, subject, content)

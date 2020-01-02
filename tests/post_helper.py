# encoding=utf-8
'''
Created on 2011-6-7

@author: wenwen
'''
import urllib
from random import Random
from multiprocessing import Process
import httplib
import urllib2
import datetime
import simplejson as json

def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0    123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str

def do_post():
    for i in range(0, 1):
        # params = urllib.urlencode({'username': 'duowan-api', 'password': "wN+%!m52;JWd'z", 'task': '{"urls":["http://att.bbs.duowan.com/avatar/042/91/86/69_avatar_big.jpg"]}' })
        # params = urllib.urlencode({'username': 'res5', 'password': 'Re@123', 'task': '{"urls":["http://res5.d.cn/ng/41/341/King_android_normal_11_S.apk"]}' })
        # params = urllib.urlencode({'username': 'snda', 'password': 'ptyy@snda.com', 'task': '{"dirs":["http://dl.autopatch.ccgslb.net/test/"],"urls":["http://dl.autopatch.ccgslb.net/test%s.jpg","http://dl.autopatch.ccgslb.net/test%s.jpg","http://dl.autopatch.ccgslb.net/test.jpg"]}' % (random_str(), random_str())})
        # params = urllib.urlencode({'username': 'snda', 'password': 'ptyy@snda.com', 'task': '{"dirs":["http://dl.autopatch.ccgslb.net/test/"]}'})
        # params = urllib.urlencode({'username': 'chinacache', 'password': 'gaS2CRW1o!', 'task': '{"urls":["http://www.chinacache.com/s.jpg","http://www.chinacache.com/s.jpg","http://www.chinacache.com/s.jpg"],"callback":{"url":"http://61.135.207.15/receiveService","acptNotice":true}}' })
        #   params = urllib.urlencode({'username': 'duowan', 'password': "925A1MMc3Jv7", 'task': '{"dirs":["http://s1.dwstatic.com/group1/M00/loadJs/"]}'})
        # import urllib
        # username = "username"
        # passwd = "pswd"
        # task = '{"urls":["http://www.xxx.com/a.jpx", "http://www.xxx  1.com/a.jpg"], "dirs":["http://www.tes.com/test/"]}'
        # params = urllib.urlencode({'username': username, 'password': passwd , 'task': task})
        # f = urllib.urlopen("http://r.chinacache.net/content/refresh" , params)

        # params = urllib.urlencode({'username': 'sina_t', 'password': 'MTE3YjU2ZTlhNmNl', 'task': '{"urls":["http://wp2.sina.cn/bmiddle/61b69811gw1dld19fhhelj.jpg",in"http://wp2.sina.cn/mw600/6f40d48agw1dpzmm9vtozj.jpg","http://wp2.sina.cn/thumbnail/6dceb033jw1doxgrr5z7hj.jpg"],"dirs":["http://wp2.sina.cn/bmiddle/test/clll/","http://wp2.sina.cn/bmiddle/testa/"]}'})
        #params = urllib.urlencode({'username': 'sina_t', 'password': 'MTE3YjU2ZTlhNmNl', 'task': '{"urls":["http://aaawp2.sina.cn/bmiddle/11.jpg","http://wp2.sina.cn/mw600/6f40d48agw1dpzmm9vtozj11.jpg","http://wp2.sina.cn/thumbnail/6dceb033jw1doxgrr5z7hj.jpg","http://wp2.sina.cn/webp720/a7272c40jw1e7lsr1sk85j20hs0npn4611.jpg"],"callback":{"url":"http://223.202.45.165/receiveService","email":["li.chang@chinacache.com","675664401@qq.com"],"acptNotice":true}}'})
        # params = urllib.urlencode({'username': 'sina_t', 'password': 'MTE3YjU2ZTlhNmNl', 'task': '{"urls":["http://wp2.sina.cn/mw600/6f40d48agw1dpzmm9vtozj11.jpg","http://wp2.sina.cn/thumbnail/6dceb033jw1doxgrr5z7hj.jpg","http://wp2.sina.cn/webp720/a7272c40jw1e7lsr1sk85j20hs0npn4611.jpg"],"callback":{"url":"http://223.202.45.165/receiveService","email":["li.chang@chinacache.com","675664401@qq.com"],"acptNotice":true}}'})
        # params = urllib.urlencode({'username': 'tuanweihui', 'password': 'TWHjpg!@#2011', 'task': '{"dirs":["http://test.tuanweihui.com/*.html","http://test.tuanweihui.com/*","http://*.tuanweihui.com/*"]}'})
        # params = urllib.urlencode({'username': 'chinacache', 'password': '1234qwerASDF#', 'task': '{"dirs":["http://www.chinacache.com/啊/","http://www.chinacache.com/发我/"],"urls":["http://www.chinacache.com/%s.jpg","http://www.chinacache.com:8080/%s.jpg","http://www.chinacache.com:8080/%s.jpg","http://www.chinacache.com:8080/我啊.jpg"],"callback":{"url":"http://223.202.52.83/receiveService","email":["dongling.zhang@chinacache.com","likun.mo@chinacache.com"],"acptNotice":true}}' % (random_str(), random_str(), random_str())})
        # params = urllib.urlencode({'username': 'chinacache', 'password': '1234qwerASDF#', 'task': '{"urls":["http://www.chinacache.com/%s.jpg","http://www.chinacache.com:8080/%s.jpg","http://www.chinacache.com:8080/%s.jpg","http://www.chinacache.com:8080/我啊.jpg"],"callback":{"url":"http://223.202.52.83/receiveService","email":["dongling.zhang@chinacache.com","likun.mo@chinacache.com"],"acptNotice":true}}' % (random_str(), random_str(), random_str())})
        # params = urllib.urlencode({'username': 'sina_t', 'password': 'MTE3YjU2ZTlhNmNl', 'task': '{"dirs":["http://ss1.sinaimg.cn/thumb321321313/"]}'})
#
        # params = urllib.urlencode({'username': 'duowan2', 'password': '123qaz?', 'task': '{"urls":["http://cdnresource.duowan.com/ofs/6lX5WrC1f9/s/gs/1422859286869687173457.png"],"callback":{"url":"","email":["huan.ma@chinacache.com","huanlema@163.com","372175901@qq.com"],"acptNotice":true}}'})
        # params = urllib.urlencode({'username': 'namibox', 'isSub': 'False', 'parent': 'namibox','type':'m-portal','task': '{"urls":["http://wr.namibox.com/tina/static/app/icon/v2/school/clickread.png"],"dirs":[]}'})
        # print 1111111111111
        # params = urllib.urlencode({'username': 'chinacache', 'password': '1234qwerASDF#', 'task': '{"dirs":["http://www.chinacache.com/啊/"]}'})
        # params = urllib.urlencode({'username': 'tttm', 'password': '4E%*^%v2T5', 'task': '{"urls":["http://file.demai.com/face/2071947/face.jpg"],"dirs":[]}'})
        # params = urllib.urlencode({'username': 'vancl', 'password': 'We@re@Team0518', 'task': '{"urls":["http://i5.vanclimg.com/others/2012/10/9/1164592541/zzk0927_64.jpg","http://www.chinacache.com:8080/%s.jpg"]}'})
        #params = urllib.urlencode({'username': 'snda', 'password': 'ptyy@snda.com', 'task': '{"dirs":["http://dl.autopatch.ccgslb.net/test/"],"urls":["http://dl.autopatch.ccgslb.net/test%s.jpg","http://dl.autopatch.ccgslb.net/test%s.jpg","http://dl.autopatch.ccgslb.net/test.jpg"]}' % (random_str(), random_str())})
        #params = urllib.urlencode({'username': 'snda', 'password': 'ptyy@snda.com', 'task': '{"dirs":["http://dl.autopatch.ccgslb.net/test/"]}'})
        # params = urllib.urlencode({'username': 'chinadaily', 'password': 'c7h1t808', 'task': '{"urls":["http://www.chinadaily.com.cn/beijing/metro_2.html","http://www.chinadaily.com.cn/beijing/metro_9.html","http://www.chinadaily.com.cn/beijing/metro_8.html"],"callback":{"url":"http://61.135.207.15/receiveService","email":["li.chang@chinacache.com","3330636@163.com"],"acptNotice":true}}' })
        # params = urllib.urlencode({'username': 'waipowang', 'password': '1q2w3e4r!', 'task': '{"dirs":["http://img3.waipowang.com/"]}'})

        # params = urllib.urlencode({'username': 'ppstream', 'password': 'ppseLean9520', 'task': '{"urls":["http://vurl.ppstv.com/ugc/5/87/532ddc48c54c9cf98c8da709275c13bf079e0fc7/532ddc48c54c9cf98c8da709275c13bf079e0fc7.pfv"],"callback":{"url":"http://www.frome.cn/1.php"}}' })
        # params = urllib.urlencode({'username': 'shws', 'password': '', 'task': '{"urls":["https://www.zhangyuelicai.com/test1/hydt/1.html"]}'})
        # params = urllib.urlencode({'username': 'edushi', 'password': '', 'task': '{"urls":["http://sz.edushi.com/bang/info/2-15-n1589961.html"]}'})
        # params = urllib.urlencode({'username': 'routon', 'password': '', 'task': '{"urls":["http://www.grandes.com.cn/video/videoinfo/7850688.xml"]}'})
        # params = urllib.urlencode({'username': 'duowan2','password': '123qaz?','task': '{"urls": ["http://download2.game.yy.com/test1/1.png"],"dirs": [""],"callback": {"url": "","email": [""] ,"acptNotice": true}}'})
        # params = urllib.urlencode({'username': '360buy','password': 'aPi@jd.com_Purge','task': '{"urls": ["http://sale.jd.com/a113.png"],"dirs": [""],"callback": {"url": "","email": [""] ,"acptNotice": false}}'})
        # task = {"urls": ["http://download.52xuexi.net/softsave/49/4/3/人教小学数学4年级上册_人民教育出版社2014年3月第1版大厂益利印刷有限公司2014年6月第1次印刷\(2.3\).zip"],"dirs": ["http://lxqncdn.miaopai.com/w132asdf.html/"], "purge_dirs": [""],"callback": {"url": "","email": [""] ,"acptNotice": False}}
        # params = urllib.urlencode({'username': 'miaopai','password': '','task': json.dumps(task)})
        # http://att2.citysbs.com/hangzhou/2017/06/25/20/middle_1200x788-202815_v2_18951498393695550_2545dfb3224210a8a10c6c4084859b37.jpg
        # params = urllib.urlencode({'username': 'lenovomm','password': 'HQ@_6752','task': '{"urls": ["http://apk.lenovomm.com/201511082220/f6a7a447e7997c648e12c622c7416981/dlserver/fileman/s3/apk/app/app-apk-lestore/5294-2015-07-13032527-1436772327717.apk?v=5&amp;clientid=409183-2-2-22-1-3-1_480_i866046024675221t19700211193547875_c20524d1p1&<autopatch>   </autopatch>mp;pn=com.stoik.mdscanvb"],"dirs": [""],"callback": {"url": "http://223.202.52.83/receiveService","email": [] ,"acptNotice": true}}'})
        # params = urllib.urlencode({'username': 'sinahouse','password': '1q@W3e$R!!!','task': '{"urls": ["http://download2.game.yy.com/cgame/client/config/game_local_scan.xml"],"dirs": [""],"callback": {"url": "","email": ["huan.ma@chinacache.com"] ,"acptNotice": true}}'})
        # # f = urllib.urlopen("http://r.chinacache.com/content/refresh" , params)
        #params = urllib.urlencode({'username': 'xiaomi', 'password': 'b63DA94cc313', 'task': '{"dirs":["http://www.aaaxiaomi.com/test/"]}'})
        task = {"urls": [
            "https://resnqa.sgmlink.com/tes1.html"],
                "dirs": [""], "purge_dirs": [""],
                "callback": {"url": "", "email": ["longjun_zhao@163.com"], "acptNotice": True}}
        params = urllib.urlencode({'username': 'sgm-ngi26', 'password': 'CYi/nekn)M', 'task': json.dumps(task)})

        print params
        # f = urllib.urlopen("https://r.chinacache.com/content/refresh" , params)
        # f = urllib.urlopen("http://192.168.225.128:6000/content/refresh" , params)
        # f = urllib.urlopen("http://223.202.52.83/content/refresh" , params)
        # f = urllib.urlopen("http://223.202.203.52:81/content/refresh" , params)
        f = urllib.urlopen("https://r.chinacache.com/content/refresh" , params)
        # f = urllib.urlopen("http://127.0.0.1/internal/refresh", params)
        print f.geturl()
        # f = urllib.urlopen("http://223.202.52.44/internal/refresh" , params)
        # f = urllib.urlopen("http://223.202.45.190/content/refresh" , params)
        #f = urllib.urlopen("http://223.202.45.166/content/refresh" , params)
        # f = urllib.urlopen("http://r.chinacache.com/content/refresh" , params)
        # f = urllib.urlopen("http://192.168.74.131/content/refresh" , params)
        # f = urllib.urlopen("http://223.202.52.77/content/refresh" , params)
        # f = urllib.urlopen("http://223.202.52.44/content/refresh" , params)
        # f = urllib.urlopen("https://r.chinacache.com/content/refresh" , params)
        # f = urllib.urlopen("http://101.251.97.214/content/refresh" , params)
        print f.read()

    # params = urllib.urlencode({'username': 'snda', 'password': 'b22b0123a7a29a6a24bb42bc785770fe', 'task': '{"dirs":["http://ik.webpatch.sdg-china.com/ik/"]}'})
    # f = urllib.urlopen("http://36.250.90.146:8090/adapter/snda_refresh" , params)
    # print f.read()


def do_3post():
    for i in range(0, 1):
        # 3.0 index
        # params = urllib.urlencode({'user': 'chinacache', 'pswd': 'chinacache', 'urls': 'http://www.chinacache.com/test.jpg%0D%0Ahttp://www.chinacache.com/noc.jpg', 'dirs':'http://www.chinacache.com/test/', 'ok':'ok'})
        # 3.0 portal
        # params = urllib.urlencode({'userID': 'mps', 'urls': '3766$http://www.mps.gov.cn/n16/n983040/n3679576/n3679621/index.html@_@3766$http://www.mps.gov.cn/n16/n983040/n3679576/index.html@_@3766$http://www.mps.gov.cn/n16/index.html@_@',  'ok':'ok'})
        # params = urllib.urlencode({'userID': 'mps', 'urls': '3766$http://www.mps.gov.cn/n16/n1282/n1720292/index.html',  'ok':'ok'})
        # 3.0 fenceng
        # params = urllib.urlencode({'user': 'snda', 'pswd': 'ptyy@snda.com', 'urls': 'http://dl.autopatch.ccgslb.net/testas.jpg%0D%0Ahttp://dl.autopatch.ccgslb.net/tessss.jpg', 'dirs':'http://dl.autopatch.ccgslb.net/test/', 'ok':'ok'})
        # params = urllib.urlencode({'userID': '792','urls': '19297$http://dl.autopatch.ccgslb.net/testas.jpg@_@19297$http://dl.autopatch.ccgslb.net/testas.jpg@_@'})

        # 3.0 portalfenceng
        # params = urllib.urlencode({'userID': 'snda', 'urls': '19297$http://dl.autopatch.ccgslb.net/testas.jpg@_@19297$http://dl.autopatch.ccgslb.net/testas.jpg@_@', 'ok':'ok'})
        # params = urllib.urlencode({'userID': 'snda', 'urls': '19297$http://dl.autopatch.ccgslb.net/testas.jpg@_@19297$http://dl.autopatch.ccgslb.net/testas.jpg@_@', 'dirs': '19297$http://dl.autopatch.ccgslb.net/test/@_@19297$http://dl.autopatch.ccgslb.net/test/a/@_@', 'ok':'ok'})


        # 3.0 chao chang
        # params = urllib.urlencode({'user': 'chinacache', 'pswd': 'chinacache', 'urls': 'http://www.chinacache.com/testaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.jpg', 'dirs':'testaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatestaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/', 'ok':'ok'})

        # 3.0 zheng ze
        # params = urllib.urlencode({'user': 'chinacache', 'pswd': 'chinacache', 'dirs':'http://www.chinacache.com/test*?/', 'ok':'ok'})

        # 3.0 portal zeng ze
        # params = urllib.urlencode({'userID': 'chinacache', 'dirs': '17098$http://www.chinacache.com/test*?/@_@', 'ok':'ok'})

        # 3.0 xin lang
       # params = urllib.urlencode({'user': 'sina_t', 'pswd': 'MTE3YjU2ZTlhNmNl', 'urls':'http://wp2.sina.cn/bmiddle/61b69811gw1dld19fhhelj.jpg%0D%0Ahttp://ww2.sinaimg.cn/mw690/aa371813jw1dzj90vjh04j.jpg', 'dirs':'http://wp2.sina.cn/bmiddle/a/', 'ok':'ok'})

        # 3.0 portal xinlang
        # params = urllib.urlencode({'userID': 'sina_t', 'urls': '15030$http://ww4.sinaimg.cn/bmiddle/test.jsp', 'ok':'ok'})
        params = urllib.urlencode({'userID': 'tuanweihui', 'dirs': '44370$http://*.tuanweihui.com/*@_@44370$http://*.tuanweihui.com/*.html', 'ok':'ok'})

        # params = urllib.urlencode({'userID': 'ekyou', 'urls': '39097$http://www.ekyou.com/81927.shtml@_@', 'ok':'ok'})

        # response = urllib.urlopen("http://60.217.249.99/index.jsp" , params)
        # response = urllib.urlopen("http://60.217.249.98/indexPortal.jsp" , params)
        # response = urllib.urlopen("http://localhost:8000" , params)

        response = urllib.urlopen("http://localhost:8000/indexPortal.jsp" , params)
        # response = urllib.urlopen("http://58.68.229.190/indexPortal.jsp" , params)
        #response = urllib.urlopen("http://ccms.chinacache.com/indexPortal.jsp" , params)
        # response = urllib.urlopen("http://61.135.207.15/indexPortal.jsp" , params)
        # hc.request('POST', '/index.jsp', params)
        # response = hc.getresponse()
        print response.read()
        # print hc.read()

def do_head():
    conn = httplib.HTTPConnection("http://localhost:8000")
    conn.request("HEAD", "/index.jsp")
    res = conn.getresponse()
    print res.status, res.reason

def postDate():

    url = 'http://58.68.228.163/cdnreport'
    urlResult = {'Submission time': datetime.datetime(2011, 9, 26, 13, 12, 1, 992000), 'Content purged': {'urls': [u'http://www.chinacache.com/uv1rCKmm.jpg:SUCCESSn']}, 'CustID': u'chinacache', 'Completion time': datetime.datetime(2011, 9, 26, 16, 22, 16, 141000), 'URL count': 1}

    a, _, b = url.partition('://')
    if b:
        domain, _, method = b.partition('/')
    else:
        domain, _, method = a.partition('/')

    hc = httplib.HTTPConnection(domain, timeout=10)
    hc.request('POST', '/' + method, str(urlResult).encode('utf-8'))
    response = hc.getresponse()
    print response.read()

if __name__ == '__main__':
    for i in range(1):
         Process(target=do_post).start()
    # postDate()
    # print urllib.urlopen('http://portal.chinacache.com/public-api/checkin.action?username=56fresh&pwd=56fresh123').read()
    # do_post()
    # params = urllib.urlencode({'username': 'chinacache', 'password': 'chinacache', 'task': '{"dirs":["http://www.chinacache.com/test/"],"callback":{"email":["3330636@163.com"]}}'})
    # f = urllib.urlopen("http://localhost:8000/content/refresh" , params)
    # print f.read()

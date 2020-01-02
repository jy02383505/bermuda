#!/usr/bin/python
#-*- coding: UTF-8 -*-
import os,os.path
import sys
import socket
try:
    import ConfigParser as configparser
except ImportError:
    import configparser

def usage():
    print '\nUsage: m [root/refresh/other] hostname'
    print '\nUsage: m list devices/receivers/worker1/worker2/worker3/shanghai'
    print '\nUsage: default user : root'
    print '\nUsage: m [username] host/hostname '
    print '\nUsage: m 223.202.52.43'
    print '\nUsage: m refresh 223.202.52.43'
    print '\nUsage: m BGP-BJ-C-5AT'
    print '\nUsage: m refresh  BGP-BJ-C-5AT'
    sys.exit(0)

# 定义用户名和密码文件
def load_config(user,name=None):
   cfg_path = os.path.join("devices.conf")
   cfg = configparser.RawConfigParser()
   cfg.read(cfg_path)
   group = 'keys'
   host = None

   password   = cfg.get(group, user)
   #id_rsa = cfg.get('connects', 'id_rsa', 'True')
   print name
   if name:
      host   = cfg.get('devices', name)
      return password,host
   return password

def show_devices(group):
    cfg_path = os.path.join("devices.conf")
    cfg = configparser.RawConfigParser()
    cfg.read(cfg_path)
    group = group
    print group
    devices   = cfg.items(group)
    print devices

def except_login(username,password,host):
    # username = 'root'
    # password = '^ZK#5y+Sznq0t(#R03Zd-6~F%s@m=L'
    # host = '223.202.52.43'
    print username,password,host
    CMD = r"""
        expect -c "
        set timeout 10
        spawn ssh -o ServerAliveInterval=60 %s@%s -p 22  ;
        expect {
           yes/no { send \"yes\r\"; exp_continue }
           *assword* { send \"%s\r\" }
        } ;
        interact"
    """%(username,host,password)
    print "cmd=", CMD
    os.system(CMD)

def ping_host(host):
    print 'ping...',host
      # use `ping` to check if the host is available now
    # 用ping的方式测试主机是否存在
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect((host, 22))
        sock.close()
        print 'The HOST is OK!'
        return True
    except:
        print 'ping: unknown host %s' % (host)
        return False
        # sys.exit(0)

def check_ip(user,hostname):
    host = None
    password = None
    print user,hostname
    if hostname.find('.')>0:
        host = hostname
        password = load_config(user)
    else:
        password,host = load_config(user,hostname)

    return password,host

def main ():
   #--list devices/receivers/worker1/worker2/worker3/shanghai
   #--host/name
    try:
        if len(sys.argv) == 1:
           usage()
        else:
            arg = sys.argv[1]
            if arg == 'list':
                group = sys.argv[2]
                if group in ["devices","receivers","worker1",\
                "worker2","worker3","shanghai"]:
                    show_devices(group)
                else:
                     usage()
            elif arg in ['root','refresh']:
                host = sys.argv[2]
                password,host = check_ip(arg,host)
                if ping_host(host):
                    except_login(arg,password,host)
            else:
                password,host = check_ip('root',arg)
                if ping_host(host):
                    except_login('root',password,host)
    except Exception,ex:
        print ex
        sys.exit(0)


if __name__ == '__main__':
   try:
       main()
   except Exception, e:
       print str(e)
       os._exit(1)

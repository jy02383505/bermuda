#!/bin/bash
file="/Application/bermuda/logs/receiver.log"
num=`tail -n100 $file|awk '{num[$8]}END{for(i in num)print i}'|wc -l`
echo "`date  '+%Y-%m-%d %T'` receiver.fcgi is active, process number:$num"
mtime=`stat -c %Y $file`
sleep 9
mtime2=`stat -c %Y $file`
if [[ $num -lt 3 || $mtime -eq $mtime2 ]]
then
        echo "`date  '+%Y-%m-%d %T'` killing recevie.fcgi"
        pid=`ps -eo pid,cmd|awk '$0~"/usr/local/bin/python ./receiver.fcg[i]"{print $1}'`
        kill $pid
        pkill -P $pid
        /Application/bermuda/bin/startup.sh receiver-restart
fi
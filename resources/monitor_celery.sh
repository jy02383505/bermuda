#!/bin/bash
cd /Application/bermuda
file="/Application/bermuda/logs/celery.log"
pidfile="/Application/bermuda/logs/celery.pid"
NOW=$(date  '+%Y-%m-%d %T')
mtime=`stat -c %Y $file`
current=`date '+%s'`
((halt=$current - $mtime))
if [[ $halt -gt 60 ]]
then
        echo "$NOW - celery halted at `stat -c %y $file`"
        echo "$NOW - killing celeryd"
        pid=`cat $pidfile`
        kill -9 $pid
        echo "$NOW - starting celeryd"
        /etc/init.d/celery.d start
else
        echo "$NOW - celeryd is active."
fi
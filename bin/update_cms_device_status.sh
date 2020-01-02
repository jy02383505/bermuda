#!/bin/bash
cd /Application/bermuda


# file="/Application/bermuda/logs/update_cms_device_status.log"
# NOW=$(date  '+%Y-%m-%d %T')
# mtime=`stat -c %Y $file`
# current=`date '+%s'`
# ((halt=$current - $mtime))


if ps -ef | grep update_cms_device_statusd | grep -v grep; then
     pid1=`ps -ef | grep update_cms_device_statusd | grep -v grep | head -1 | awk '{print $2}'`
     echo "update_cms_device_statusd is running!  main process id = $pid1"
else
    echo "update_cms_device_statusd will be running ..."
    ./bin/update_cms_device_statusd
fi
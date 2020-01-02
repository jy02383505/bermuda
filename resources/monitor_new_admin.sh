#!/bin/bash

a=`ps -ef|grep new_admin|grep -v grep |awk '{print $2}'` x

if [[ $a != x ]]
then
    echo "`date  '+%Y-%m-%d %T'` new_admin is active!"
else
    echo "`date  '+%Y-%m-%d %T'` new_admin is down!"
    echo "`date  '+%Y-%m-%d %T'` start new_admin"
    /Application/bermuda/bin/startup.sh admin-restart
fi
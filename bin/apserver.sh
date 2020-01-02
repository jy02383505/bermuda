#!/bin/bash
cd /Application/bermuda

if ps -ef | grep apserverd | grep -v grep; then 
     pid1=`ps -ef | grep apserverd | grep -v grep | head -1 | awk '{print $2}'`
     echo "apserverd is running!  main process id = $pid1"
else
    echo "apserverd is running ..."
    nohup ./bin/apserverd &
fi

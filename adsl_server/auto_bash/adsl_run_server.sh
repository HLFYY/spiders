#!/bin/sh
PATH=/root/venv/python3-forcrawl/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin

curday=`date +%Y-%m-%d-%H%M%S`
server_process_name="adsl_server.py"
cd /root/code/spiders/adsl_server
ps -fe|grep $server_process_name |grep -v grep
if [ $? -ne 0 ]
then
    python $server_process_name >> /dev/null 2>&1 &
    echo "$server_process_name start process.....$curday"
else
    echo "runing....."
fi
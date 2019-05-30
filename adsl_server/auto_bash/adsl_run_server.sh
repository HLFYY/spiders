#!/bin/sh
PATH=/root/venv/python3-forcrawl/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin

server_process_name="adsl_server.py"
cd /root/code
ps -fe|grep $server_process_name |grep -v grep
if [ $? -ne 0 ]
then
    python $server_process_name >> /data/logs/server/adsl_server.log 2>&1 &
    echo "$server_process_name start process.....$curday"
else
    echo "runing....."
fi
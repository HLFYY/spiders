#!/bin/sh
PATH=/root/venv/python3-forcrawl/bin:/root/perl5/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin

cd /root/code
python client.py >> /data/logs/server/adsl-client.log 2>&1 &
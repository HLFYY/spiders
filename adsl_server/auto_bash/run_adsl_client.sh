#!/bin/sh
PATH=/root/venv/python3-forcrawl/bin:/root/perl5/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin

cd /root/code/spiders/adsl_server
python adsl_client.py >> /dev/null 2>&1 &
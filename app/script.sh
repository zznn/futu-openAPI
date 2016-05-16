#! /bin/sh

ostr=`cat db.py | grep 'host' |awk -F "'" '{print $4}'`

var=`cat /etc/hosts | grep 'futudb' | awk '{print $1}'`

sed -i "s/${ostr}/${var}/g" db.py

nginx;

gunicorn mainapp:app -b 127.0.0.1:4000 -w 4 --log-level=debug

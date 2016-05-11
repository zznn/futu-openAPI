#! /bin/sh
nginx;
gunicorn -w 4 -b 127.0.0.1:4000 mainapp:app

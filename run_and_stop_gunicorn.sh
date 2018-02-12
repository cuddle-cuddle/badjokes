#!/usr/bin/env bash

gunicorn --timeout 600 --pid gunicorn.pid hello-world:app &
sleep 1
kill -TERM `cat gunicorn.pid`
wait

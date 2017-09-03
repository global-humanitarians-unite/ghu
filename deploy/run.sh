#!/bin/bash
exec uwsgi --module ghu_web.wsgi:application -s sock --umask 0

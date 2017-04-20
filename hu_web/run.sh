#!/bin/bash
exec uwsgi --module hu_web.wsgi:application -s sock --umask 0

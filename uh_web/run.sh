#!/bin/bash
exec uwsgi --module uh_web.wsgi:application -s sock --umask 0

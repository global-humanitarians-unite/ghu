#!/bin/bash

[[ -z $GHU_DEPLOY_CONFIG_PATH ]] && {
    printf 'error: $GHU_DEPLOY_CONFIG_PATH is not set. Set it to the path to '`
          `'deploy.config and try again\n' >&2
    exit 1
}

. "$GHU_DEPLOY_CONFIG_PATH"

venv="$deploy_root/venv"
worktree="$deploy_root/worktrees/current"

exec "$venv/bin/uwsgi" --virtualenv "$venv" \
                       --module ghu_web.wsgi:application \
                       --pythonpath "$worktree/ghu_web" \
                       --socket "$deploy_root/sock/uwsgi.sock" \
                       --umask 0
